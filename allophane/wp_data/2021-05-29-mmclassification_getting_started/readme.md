---
title: "MMClassification_Getting_Started"
date: "2021-05-29"
categories: 
  - "allophane"
  - "extracurricular"
---

## 准备数据集

建议将数据集根符号链接到`$MMCLASSIFICATION/data`. 如果您的文件夹结构不同，您可能需要更改配置文件中的相应路径。  
说人话就是建议把数据集放在mmclassification/data文件目录下，不然你还得专门改，默认支持imagenet、cifar、mnist

```
mmclassification
├── mmcls
├── tools
├── configs
├── docs
├── data
│   ├── imagenet
│   │   ├── meta
│   │   ├── train
│   │   ├── val
│   ├── cifar
│   │   ├── cifar-10-batches-py
│   ├── mnist
│   │   ├── train-images-idx3-ubyte
│   │   ├── train-labels-idx1-ubyte
│   │   ├── t10k-images-idx3-ubyte
│   │   ├── t10k-labels-idx1-ubyte
```

对于 ImageNet，它有多个版本，但最常用的是[ILSVRC 2012](http://www.image-net.org/challenges/LSVRC/2012/)。可以通过以下步骤访问它。

1. 注册一个帐户并登录到[下载页面](http://www.image-net.org/download-images)。
2. 找到ILSVRC2012的下载链接，下载以下两个文件
    - ILSVRC2012\_img\_train.tar (~138GB)
    - ILSVRC2012\_img\_val.tar (~6.3GB)
3. 解压下载的文件
4. 使用此[脚本](https://github.com/BVLC/caffe/blob/master/data/ilsvrc12/get_ilsvrc_aux.sh)下载元数据

对于 MNIST、CIFAR10 和 CIFAR100，如果找不到数据集，将自动下载并解压缩。  
自定义数据集的使用请参考[教程2：添加新数据集](https://mmclassification.readthedocs.io/en/latest/tutorials/new_dataset.html)。或者（算了，我还没写）

使用预训练模型进行推理  
在mmclassification的**[模型动物园](https://github.com/open-mmlab/mmclassification/blob/master/docs/model_zoo.md)**（什么鬼名字）里找预训练模型可进行推理，来这里

## 推断单个图像

```
python demo/image_demo.py ${IMAGE_FILE} ${CONFIG_FILE} ${CHECKPOINT_FILE}
```

这三个$对应图像文件路径、config文件、checkpoint文件（也就是预训练模型文件）

## 推断和测试数据集

仅介绍单 GPU的，至于GPU看[文档](https://mmclassification.readthedocs.io/en/latest/getting_started.html#inference-and-test-a-dataset)！

```
# single-gpu
python tools/test.py ${CONFIG_FILE} ${CHECKPOINT_FILE} [--metrics ${METRICS}] [--out ${RESULT_FILE}]
```

可选参数：

- `RESULT_FILE`: 输出结果的文件名。如果未指定，则结果将不会保存到文件中。支持格式包括 json、yaml 和 pickle（即.pkl文件，需要pickle库打开，比如）

```
f=open(path,'rb')
data=pickle.load(f)
print(data)
```

- `METRICS`：对结果进行评价的项目，如准确率、准确率、召回率等。accuracy, precision, recall,

例：假设您已经将检查点下载到目录中`checkpoints/`。在 ImageNet 验证集上推断 ResNet-50 以获得预测标签及其相应的预测分数。

```
python tools/test.py configs/imagenet/resnet50_batch256.py checkpoints/xxx.pth --out result.pkl
```

## 训练模型

MMClassification实现了分布式训练和非分布式训练，分别使用MMDistributedDataParallel和MMDataParallel完成。

所有输出（日志文件和检查点）都将保存到工作目录中，该目录由`work_dir`配置文件中指定。  
默认情况下，我们在每个 epoch 之后在验证集上评估模型，您可以通过在训练的config文件中添加 interval 参数来更改评估间隔。

```
evaluation = dict(interval=12)  # This evaluate the model per 12 epoch.
```

## 使用单个 GPU 进行训练

```
python tools/train.py ${CONFIG_FILE} [optional arguments]
```

\[optional arguments\]包括：

- `--no-validate`（**不建议**）：默认情况下，代码库将在训练期间每 k（默认值为 1）个 epoch 执行一次评估。若要禁用此行为，请使用`--no-validate`。
- `--work-dir ${WORK_DIR}`: 覆盖配置文件中指定的工作目录。
- `--resume-from ${CHECKPOINT_FILE}`：从以前的检查点文件恢复。（其实就是在训练一半的模型基础上训练啦）

`resume-from`和load-from之间的差异：   
`resume-from` 加载模型权重和优化器状态，并且 epoch 也从指定的检查点继承。 它通常用于恢复意外中断的训练过程。  
`load-from` 只加载模型权重，训练epoch从0开始，通常用于调优。

## 有用的工具

我们提供了一个改编自[flops-counter.pytorch](https://github.com/sovrasov/flops-counter.pytorch)的脚本来计算给定模型的 FLOP 和参数。

```
python tools/get_flops.py ${CONFIG_FILE} [--shape ${INPUT_SHAPE}]
```

你会得到这样的结果。

```
==============================
Input shape: (3, 224, 224)
Flops: 4.12 GFLOPs
Params: 25.56 M
==============================
```

**注意**：此工具仍处于实验阶段，我们不保证数字正确。您可以很好地将结果用于简单的比较，但在技术报告或论文中采用它之前，请仔细检查它。

(1) FLOPs 与输入形状有关，而参数则无关。默认输入形状为 (1, 3, 224, 224)。  
(2) 一些算子不计入 FLOP，如 GN 和自定义算子。详情请参阅[`mmcv.cnn.get_model_complexity_info()`](https://github.com/open-mmlab/mmcv/blob/master/mmcv/cnn/utils/flops_counter.py)。

### 发布模型

在将模型上传到 AWS 之前，您可能需要 (1) 将模型权重转换为 CPU 张量 (2) 删除优化器状态 (3) 计算检查点文件的哈希并将哈希 ID 附加到文件名。

```
python tools/publish_model.py ${INPUT_FILENAME} ${OUTPUT_FILENAME}
```

例如

```
python tools/publish_model.py work_dirs/resnet50/latest.pth imagenet_resnet50_20200708.pth
```

最终输出文件名将是.`imagenet_resnet50_20200708-{hash id}.pth`
