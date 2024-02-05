---
title: "Add_SA_to_cycleGAN"
date: "2022-04-13"
categories: 
  - "allophane"
  - "extracurricular"
---

因为去整seg再加上BME会议导致这玩意忘了写一下

首先在model/network>defineG()添加

```
    elif netG == 'SA_resnet_1blocks':
        net = SA_ResnetGenerator(input_nc, output_nc, ngf, norm_layer=norm_layer, use_dropout=use_dropout, n_blocks=1)
```

然后在model/network 追加类 SA\_ResnetGenerator 复制于ResnetGenerator ,更改下面的地方

```
for i in range(n_blocks):       # add ResNet blocks
    model += [ResnetBlock(ngf * mult, padding_type=padding_type, norm_layer=norm_layer, use_dropout=use_dropout, use_bias=use_bias)]
```

org

```
for i in range(n_blocks):       # add ResNet blocks
    model += [SA_ResnetBlock(ngf * mult, padding_type=padding_type, norm_layer=norm_layer, use_dropout=use_dropout, use_bias=use_bias)]
```

update

然后在 model/network 追加类 SA\_ResnetBlock 复制于ResnetBlock,并引入类 Self\_Attn  
首先是init中追加Self\_Attn

```
class SA_ResnetBlock(nn.Module):
    """Define a Resnet block"""

    def __init__(self, dim, padding_type, norm_layer, use_dropout, use_bias):
        """Initialize the Resnet block

        A resnet block is a conv block with skip connections
        We construct a conv block with build_conv_block function,
        and implement skip connections in <forward> function.
        Original Resnet paper: https://arxiv.org/pdf/1512.03385.pdf
        """
        super(SA_ResnetBlock, self).__init__()
        self.conv_block = self.build_conv_block(dim, padding_type, norm_layer, use_dropout, use_bias)
        self.self_attn = Self_Attn(dim, 'relu')
```

然后更改SA\_ResnetBlock中的build\_conv\_block()方法  
众所周知,这个resblock里的一通操作只是为了:

选择加什么边 (个人强烈建议用 ReplicationPad2d, 选直接补0的也行)  
一个卷积  
dropout(0.5) ( 然而它默认是不使用,那我也不加了吧)  
选择加什么边 (同上)  
一个卷积

那我们就把原来的卷积后面再追加就完事了

```
        conv_block += [nn.Conv2d(dim, dim, kernel_size=3, padding=p, bias=use_bias), norm_layer(dim), nn.ReLU(True)]
        conv_block += [self.self_attn]
```

然后为了防止错误,把self\_attn的前传改一下(仅输出同大小特征图)

```
    def forward(self, x):
        """
            inputs :
                x : input feature maps( B X C X W X H)
            returns :
                out : self attention value + input feature
                attention: B X N X N (N is Width*Height)
        """
        m_batchsize, C, width, height = x.size()
        proj_query = self.query_conv(x).view(m_batchsize, -1, width * height).permute(0, 2, 1)  # B X CX(N)
        proj_key = self.key_conv(x).view(m_batchsize, -1, width * height)  # B X C x (*W*H)
        energy = torch.bmm(proj_query, proj_key)  # transpose check
        attention = self.softmax(energy)  # BX (N) X (N)
        proj_value = self.value_conv(x).view(m_batchsize, -1, width * height)  # B X C X N

        out = torch.bmm(proj_value, attention.permute(0, 2, 1))
        out = out.view(m_batchsize, C, width, height)

        out = self.gamma * out + x
        return out
```

最后把原network.py替换

现在打印一个SA\_resblock 的生成器是

```
DataParallel(
  (module): SA_ResnetGenerator(
    (model): Sequential(
      (0): ReflectionPad2d((3, 3, 3, 3))
      (1): Conv2d(3, 64, kernel_size=(7, 7), stride=(1, 1))
      (2): InstanceNorm2d(64, eps=1e-05, momentum=0.1, affine=False, track_running_stats=False)
      (3): ReLU(inplace=True)
      (4): Conv2d(64, 128, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1))
      (5): InstanceNorm2d(128, eps=1e-05, momentum=0.1, affine=False, track_running_stats=False)
      (6): ReLU(inplace=True)
      (7): Conv2d(128, 256, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1))
      (8): InstanceNorm2d(256, eps=1e-05, momentum=0.1, affine=False, track_running_stats=False)
      (9): ReLU(inplace=True)
      (10): SA_ResnetBlock(
        (self_attn): Self_Attn(
          (query_conv): Conv2d(256, 32, kernel_size=(1, 1), stride=(1, 1))
          (key_conv): Conv2d(256, 32, kernel_size=(1, 1), stride=(1, 1))
          (value_conv): Conv2d(256, 256, kernel_size=(1, 1), stride=(1, 1))
          (softmax): Softmax(dim=-1)
        )
        (conv_block): Sequential(
          (0): ReflectionPad2d((1, 1, 1, 1))
          (1): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1))
          (2): InstanceNorm2d(256, eps=1e-05, momentum=0.1, affine=False, track_running_stats=False)
          (3): ReLU(inplace=True)
          (4): Self_Attn(
            (query_conv): Conv2d(256, 32, kernel_size=(1, 1), stride=(1, 1))
            (key_conv): Conv2d(256, 32, kernel_size=(1, 1), stride=(1, 1))
            (value_conv): Conv2d(256, 256, kernel_size=(1, 1), stride=(1, 1))
            (softmax): Softmax(dim=-1)
          )
          (5): ReflectionPad2d((1, 1, 1, 1))
          (6): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1))
          (7): InstanceNorm2d(256, eps=1e-05, momentum=0.1, affine=False, track_running_stats=False)
          (8): Self_Attn(
            (query_conv): Conv2d(256, 32, kernel_size=(1, 1), stride=(1, 1))
            (key_conv): Conv2d(256, 32, kernel_size=(1, 1), stride=(1, 1))
            (value_conv): Conv2d(256, 256, kernel_size=(1, 1), stride=(1, 1))
            (softmax): Softmax(dim=-1)
          )
        )
      )
      (11): ConvTranspose2d(256, 128, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), output_padding=(1, 1))
      (12): InstanceNorm2d(128, eps=1e-05, momentum=0.1, affine=False, track_running_stats=False)
      (13): ReLU(inplace=True)
      (14): ConvTranspose2d(128, 64, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), output_padding=(1, 1))
      (15): InstanceNorm2d(64, eps=1e-05, momentum=0.1, affine=False, track_running_stats=False)
      (16): ReLU(inplace=True)
      (17): ReflectionPad2d((3, 3, 3, 3))
      (18): Conv2d(64, 3, kernel_size=(7, 7), stride=(1, 1))
      (19): Tanh()
    )
  )
```

PS: 这东西可不能这么塞(扩大复杂度得到的精度提高和说DenseBlock比ResBlock性能高，所以DenseBlock全面碾压ResBlock一样耍流氓)  
建议把resblock里的两个conv替换成一个SA  
或者之后直接将一个resblock换成一个SA  
再或者在上面的基础上把SA的value\_conv()换成3\*3的并把resblock的补边方式继承到value\_conv上  
又或者类似原文，在后面几个结束时候的常规卷积(256>128>64>3)之间塞
