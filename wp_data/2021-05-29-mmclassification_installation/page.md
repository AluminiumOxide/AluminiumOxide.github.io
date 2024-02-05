---
title: "MMClassification_Installation"
date: "2021-05-29"
categories: 
  - "allophane"
  - "extracurricular"
---

首先我默认所有人（算了根本没人(╯‵□′)╯︵┻━┻）看过[win10安装mmcv-full](http://aluminium/allophane.com/index.php/2021/05/26/win10_build_mmcv-full_from_source/)这篇文章，  
哦，你用linux啊，那没事了

## 环境要求

- Python 3.6+
- PyTorch 1.3+
- [MMCV](https://github.com/open-mmlab/mmcv)

有关MMCV的版本匹配，看了之前的应该已经不用了

| MMClassification version | MMCV version |
| --- | --- |
| master | mmcv>=1.3.1, <=1.5.0 |
| 0.11.1 | mmcv>=1.3.1, <=1.5.0 |
| 0.11.0 | mmcv>=1.3.0 |
| 0.10.0 | mmcv>=1.3.0 |
| 0.9.0 | mmcv>=1.1.4 |
| 0.8.0 | mmcv>=1.1.4 |
| 0.7.0 | mmcv>=1.1.4 |
| 0.6.0 | mmcv>=1.1.4 |

## 安装MMClassification

创建 conda 虚拟环境要是没创建，那就按照下面

```
conda create -n open-mmlab python=3.7 -y
conda activate open-mmlab
```

安装PyTorch 和 torchvision，参考[官方说明](https://pytorch.org/)，或者参考之前[安装mmdet2.6](http://aluminium/allophane.com/index.php/2020/12/09/mmdetection2-6-win10-without-cuda-install/)的pytorch安装，例如：（写这个的时候这个例子应该是1.8.1？）

```
conda install pytorch torchvision -c pytorch
```

克隆 mmclassification （我直接建议你进入[github](https://github.com/open-mmlab/mmclassification.git)，然后下载zip解压进入）

```
git clone https://github.com/open-mmlab/mmclassification.git
cd mmclassification
```

安装环境要求，并安装mmcls（注意那个点 “.”）

```
pip install -e .  # or "python setup.py develop"
```

以下为直接机翻 笔记：

1. 按照上面的说明，mmclassification是安装在`dev` mode上的，对代码所做的任何本地修改都会生效，不需要重新安装（除非你提交了一些提交并想要更新版本号）。
2. 如果您想使用`opencv-python-headless`代替`opencv-python`，您可以在安装[mmcv](https://github.com/open-mmlab/mmcv)之前安装[它](https://github.com/open-mmlab/mmcv)。

使用多个 MMClassification 版本忽略
