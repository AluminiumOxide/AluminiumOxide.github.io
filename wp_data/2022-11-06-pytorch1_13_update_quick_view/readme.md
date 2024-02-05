---
title: "pytorch1_13_Update_Quick_View"
date: "2022-11-06"
categories: 
  - "blog"
  - "allophane"
---

直接进入官网下载[Start Locally | PyTorch](https://pytorch.org/get-started/locally/)

提前留好位置，环境安装完接近个7G

```
conda create -n torch113 python=3.8
conda install pytorch torchvision torchaudio pytorch-cuda=11.6 -c pytorch -c nvidia
```

**pytorch1.13更新的完整内容请参考[PyTorch 1.13 release](https://pytorch.org/blog/PyTorch-1.13-release/)**  
**以及pytorch类库的对应更新内容请参考[New Library Updates in PyTorch 1.13](https://pytorch.org/blog/new-library-updates-in-pytorch-1.13/)**

首先将PyTorch更新内容翻译成白话，就是：

| Stable | Beta | Prototype |
| --- | --- | --- |
| 绝美的BetterTransformer(虽然训练时没法加速) | 现在pytorch可以在Intel VTune Profiler上可视化模型的性能了 | torch对 Arm计算库的支持越走越远辣 |
| 我们为了C++17抛弃了cuda10.2和11.3这两个老朋友 | 现在支持channel-last 格式数组和 bf16格式的数据了 | 现在可以用CUDA Sanitizer自动寻找数据错误辣 |
|  | Functorch 被强按进了PyTorch 中 |  |
|  | 脸书正在和苹果进行深度的py交易 |  |

其实对于正常玩家，stable就差不多够用了，至于说beta和night版，其实如果不是特殊需要用处不是特别多

我们只需要知道**新版本调用torch亲手调教的多头自注意力机制(可能)更舒服了，并且没更新cuda的得更新了**

至于说VTune Profile分析模型性能、支持channel-last格式和16位浮点数、进一步整合pytorch库、和苹果、英特尔、ARM的py交易、cuda自查错误，这些其实影响不是特别大

而且看的出来现在torch专注于开发跨所有领域的通用和可扩展 API，类库的更新内容比torch的更新内容还多，那么这里就把(我个人感觉有意思)的放在这个表里了

<table><tbody><tr><td><strong>Library</strong></td><td><strong>更新内容</strong></td></tr><tr><td>TorchAudio</td><td>新增 Hybrid Demucs 模型和 新数据集</td></tr><tr><td>TorchData</td><td><strong>DataLoader2(Night) </strong><strong>引入</strong><strong>DataPipe</strong><strong>图</strong><strong>,</strong><strong>支持动态分片用于多进程</strong><strong>/</strong><strong>分布式数据加载、多个后端阅读服务和</strong><strong>DataPipe</strong><strong>图动态修改</strong></td></tr><tr><td>torch::deploy</td><td>(Beta)允许在单个进程中运行多个 Python 解释器</td></tr><tr><td>TorchEval</td><td>(Night) 评估机器学习模型的用户构建的库&nbsp; # 12月呢,别急</td></tr><tr><td>TorchMultimodal</td><td>(Beta) 用于大规模训练 SoTA 多任务多模式模型的 PyTorch 域库&nbsp; # 11月呢,别急</td></tr><tr><td>TorchRec</td><td>简化的优化器融合(Night)、对嵌入模块进行分片(Beta)、Quantized Comms混合精度加速(Beta)</td></tr><tr><td>TorchSnapshot</td><td>(Beta)<strong>用于 </strong><strong>PyTorch</strong><strong> </strong><strong>应用程序的高性能的检查库</strong></td></tr><tr><td>TorchVision</td><td>新的模型注册 API(Beta)&nbsp;、增加MViT和S3D视频分类模型(Beta)、增加Swin Transformer V2和MaxViT转换器分类模型(Stable)</td></tr><tr><td>Torch-TensorRT</td><td>允许直接在 PyTorch 中优化模型以进行部署提升性能(Night)</td></tr><tr><td>TorchX</td><td>列表 API、实验跟踪、弹性训练和改进的调度程序支持</td></tr></tbody></table>

有关bettertransformer的内容[A BetterTransformer for Fast Transformer Inference | PyTorch](https://pytorch.org/blog/a-better-transformer-for-fast-transformer-encoder-inference/)

视频里用到的脚本，得额外装一下tensorboard

```
from torch import nn
import torch
from torch.utils.tensorboard import SummaryWriter


def demo_EncoderLayer():
    encoder_layer = nn.TransformerEncoderLayer(d_model=512, nhead=8)
    src = torch.rand(10, 32, 512)
    out = encoder_layer(src)

    writer = SummaryWriter()
    writer.add_graph(encoder_layer,src)
    writer.close()
    pass


def demo_Encoder():
    encoder_layer = nn.TransformerEncoderLayer(d_model=512, nhead=8)
    transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=6)
    src = torch.rand(10, 32, 512)
    out = transformer_encoder(src)

    writer = SummaryWriter()
    writer.add_graph(transformer_encoder,src)
    writer.close()
    pass


def demo_multihead_attn():
    src = torch.rand(11, 23, 512)
    src2 = torch.rand(11, 29, 512)
    multihead_attn = nn.MultiheadAttention(embed_dim=512, num_heads=8,batch_first=True)
    attn_output, attn_output_weights = multihead_attn(query=src, key=src2, value=src2)

    writer = SummaryWriter()
    writer.add_graph(multihead_attn, [src, src2, src2])
    writer.close()
    pass


if __name__ == '__main__':
    demo_multihead_attn()
    demo_EncoderLayer()
    demo_Encoder()
    pass
```
