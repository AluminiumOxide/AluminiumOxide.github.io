---
title: "Anaconda_Prompt_常用命令"
date: "2021-01-24"
categories: 
  - "allophane"
  - "extracurricular"
---

| 功能 | 命令 |
| --- | --- |
| 查询conda的命令使用 | conda -h |
| 查询conda版本 | conda --version |
| 创建虚拟环境 | conda create -n 环境名称 python=3.7（python版本） |
| 删除虚拟环境 | conda remove -n 环境名称 --all |
| 激活虚拟环境 | conda activate 环境名称（如果不添环境名称那就是激活base环境） |
| 关闭虚拟环境 | conda deactivate |
| 克隆虚拟环境 | conda create -n 新环境 --clone 旧环境 |
| 查看已安装的库 | conda list |
| 列出当前已有环境 | conda env list 或 conda info -e |
| 添加环境中某个库 | conda install 包名称 （已进入虚拟环境内） |
| 更新环境中某个库 | conda update 包名称（已进入虚拟环境内） |
| 删除环境中某个库 | conda remove 包名称（已进入虚拟环境内） |
| 删除环境中某个库及以下所有包 | conda remove -n 环境名称 --all |
| 查看已存在虚拟环境 | conda env list |
| 安装库 | pip install 名称 -i https://pypi.tuna.tsinghua.edu.cn/simple（使用镜像） |
| 安装指定版本的库 | pip install 名称==版本 --user(如，pip install pillow==6.2.2 --user） |
| 打开jupyter book | jupyter notebook |
| 添加Anaconda的TUNA镜像 | conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ |
