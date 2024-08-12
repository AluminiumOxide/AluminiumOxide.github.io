首先安装cmake

```
conda install -c anaconda cmake
```

先把国内镜像删除再说，不然找不到

```
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
  
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  
channel_alias: http://mirrors.tuna.tsinghua.edu.cn/anaconda
```

安装

![image-20240725104946909](conda_env_triton/image-20240725104946909.png)

```
pip install ninja cmake wheel
conda install nvidia/label/cuda-12.5.1::cuda-nvcc
```

