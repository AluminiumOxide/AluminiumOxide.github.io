---
title: "change_cuda_version"
date: "2022-03-19"
categories: 
  - "blog"
  - "allophane"
---

由于最近需要使用tensorflow，突然发现以前安的cuda10.2好臭啊！！！！！！！

![](images/image-17.png)

重新安了cuda10.0（略，具体请查看[先前文章](http://aluminium/allophane.com/index.php/2021/05/04/about_cuda_install/)）

然后系统变量里cudapath换成10.0

![](images/image-18.png)

顺带着说一下环境变量太大了怎么办

![](images/N94481DM6T3QOKTB.png)

创建一个别的环境变量然后把没用的扔进去

![](images/image-19.png)

![](images/image-20.png)

然后把cuda10.0塞到前面（嚣张）

![](images/image-21.png)

OK，记得切一个新的cmd测试

![](images/image-22.png)
