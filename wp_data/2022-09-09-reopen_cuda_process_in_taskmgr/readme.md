---
title: "Reopen_cuda_process_in_Taskmgr"
date: "2022-09-09"
categories: 
  - "blog"
  - "allophane"
---

由于换了电脑导致任务管理器里没法直接看cuda占用，所以

![](images/image-edited.png)

进到 设置/系统/屏幕/显示卡/默认图形设置  
把硬件加速GPU计划关掉

![](images/image.png)

重启后OK

![](images/image-1.png)

也别太担心，这个加速计划基本上是打游戏时候让CPU给GPU帮忙用的（大概可以这么理解）  
至于说敲die码时有多少影响？影响个锤子，关了就关了  
\# 要不是win没有linux的watch
