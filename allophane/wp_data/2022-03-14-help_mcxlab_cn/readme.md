---
title: "help_mcxlab_CN"
date: "2022-03-14"
categories: 
  - "allophane"
  - "extracurricular"
---

可以理解成MCXLAB只是一个MC模拟工具，主要调用函数的方式就是直接mcxlab，后续是输入输出参数设置

 Format:
     fluence=mcxlab(cfg);
        or
     \[fluence,detphoton,vol,seed,trajectory\]=mcxlab(cfg);
     \[fluence,detphoton,vol,seed,trajectory\]=mcxlab(cfg, option);

输入部分

- cfg
    - 结构体或结构体数组。 cfg 的每个元素都定义了与模拟相关的参数。
    - if cfg='gpuinfo': 返回支持的 GPU 及其参数
- option(可选)
    - options 是一个字符串，指定附加选项
    - option='preview'：使用 mcxpreview(cfg) 绘制域配置
    - option='mcxcl'：这在非 NVIDIA 硬件上调用 mcxcl.mex\* 而不是 mcx.mex\*

cfg 必须包含以下字段：

<table><tbody><tr><td>参数名称</td><td>描述</td></tr><tr><td>*cfg.nphoton</td><td>要模拟的光子总数（整数）<br>最大支持值为 2^63-1</td></tr><tr><td>*cfg.vol</td><td>指定域中媒体索引的 3D 数组。<br>可以是 uint8、uint16、uint32、单或双数组。<br>如果 cfg.vol 具有单一维度（在 x 或 y 中），则支持 2D 模拟；在这种情况下，srcpos/srcdir 必须属于 2D 平面。</td></tr><tr><td>*cfg.prop</td><td>一个 N×4 数组，每行按顺序指定 [mua, mus, g, n]。<br>第一行对应于介质类型 0（背景），通常为 [0 0 1 1]。第二行是类型 1，依此类推。<br>背景介质（类型 0）具有特殊含义：光子在从非零体素移动到零体素时终止。</td></tr><tr><td>*cfg.tstart</td><td>模拟的开始时间（以秒为单位）</td></tr><tr><td>*cfg.tstep</td><td>模拟的时间门宽度（以秒为单位）</td></tr><tr><td>*cfg.srcpos</td><td>一个 1 x 3 向量，网格单元中源的位置</td></tr><tr><td>*cfg.srcdir</td><td>一个1×3的向量，指定事件向量； 如果 srcdir 包含第 4 个元素，它指定源的焦距（仅对可聚焦的 src 有效，例如平面、圆盘、傅立叶、高斯、图案、狭缝等）；<br>如果焦距为 nan，则无论 srcdir 方向如何，所有光子都将各向同性地发射。</td></tr></tbody></table>

% mua Absorption coefficient (1/mm) for each Domain 每个域的吸收系数 (1/mm)  
% mus Scattering coefficient (1/mm) for each Domain 每个域的散射系数 (1/mm)  
% g Scattering anisotropy for each Domain 每个域的散射各向异性  
% n Index of refraction for each Domain 每个域的折射率

\== MC 模拟设置 == (可选)

<table><tbody><tr><td>参数名称</td><td>描述</td></tr><tr><td>cfg.seed</td><td>随​​机数生成器的种子（整数）[0]<br>如果设置为 uint8 数组，则每列中的二进制数据用于生成光子（即“重播”模式）<br>示例：demo_mcxlab_replay.m</td></tr><tr><td>cfg.respin</td><td>在给定时间内重复模拟（整数）[1]<br>如果为负，则将总光子数划分为重新旋转子集</td></tr><tr><td>cfg.isreflect</td><td>[1]-考虑折射率不匹配，0-匹配折射率</td></tr><tr><td>cfg.bc</td><td>per-face 边界条件 (BC)，一个 6 个字母的字符串，用于在 -x、-y、-z、+x、+y、+z 轴处的边界框面；<br>如果给定，则覆盖 cfg.isreflect。每个字母可以是以下之一：<br>'_'：未定义，回退到 cfg.isreflect<br>'r'：像 cfg.isreflect=1，菲涅耳反射 BC<br>'a'：像cfg.isreflect=0，总吸收BC<br>'m'：镜面或全反射 BC<br>'c': 循环 BC，从对面进入</td></tr><tr><td>cfg.isnormalized</td><td>[1]-将输出能量归一化为单一源，0-无反射</td></tr><tr><td>cfg.isspecular</td><td>1-如果源在外面，则计算镜面反射，[0] 没有镜面反射</td></tr><tr><td>cfg.maxgate</td><td>每次模拟的时间门数</td></tr><tr><td>cfg.minenergy</td><td>当重量小于这个水平（浮动）[0.0]时终止光子</td></tr><tr><td>cfg.unitinmm</td><td>定义网格边长 [1.0] 的长度单位<br>示例：demo_sphere_cube_subpixel.m</td></tr><tr><td>cfg.shapes</td><td>用于网格中其他形状的 JSON 字符串<br>示例：demo_mcxyz_skinvessel.m</td></tr><tr><td>cfg.gscatter</td><td>在光子完成指定数量的散射事件后，mcx 然后忽略各向异性 g，仅针对速度执行各向同性散射 [1e9]</td></tr></tbody></table>

\== GPU settings ==

<table><tbody><tr><td></td><td></td></tr><tr><td>cfg.autopilot</td><td>1-自动设置线程和块，[0]-使用nthread/nblocksize</td></tr><tr><td>cfg.nblocksize</td><td>要使用多少个 CUDA 线程块 [64]</td></tr><tr><td>cfg.nthread</td><td>CUDA 线程总数 [2048]</td></tr><tr><td>cfg.gpuid</td><td>使用哪个 GPU（运行“mcx -L”列出所有 GPU）[1]<br>如果设置为整数，则 gpuid 指定用于模拟的 GPU 的索引（从 1 开始）；<br>如果设置为由 1 和 0 组成的二进制字符串，则启用多个 GPU。例如，“1101”<br>允许一起使用第 1、第 2 和第 4 个 GPU。<br>示例：mcx_gpu_benchmarks.m</td></tr><tr><td>cfg.workload</td><td>一个数组，表示每个选定 GPU 的相对负载。<br>例如，[50,20,30] 分别为 3 个选定的 GPU 分配 50%、20% 和 30% 的光子； [10,10] 在 2 个活动 GPU 之间平均分配负载。一个简单的负载平衡策略是使用 GPU 核心数作为权重。</td></tr><tr><td>cfg.isgpuinfo</td><td>1-打印 GPU 信息，[0]-不打印</td></tr></tbody></table>

\== 源检测器参数 ==

<table><tbody><tr><td></td><td></td></tr><tr><td>cfg.detpos</td><td>一个 N x 4 数组，每行指定一个检测器：[x,y,z,radius]</td></tr><tr><td>cfg.maxdetphoton</td><td>探测器保存的最大光子数 [1000000]</td></tr><tr><td>cfg.srctype</td><td>源类型，src的参数由cfg.srcparam{1,2}指定，标有 [*] 的源类型可以使用焦距参数（cfg.srcdir 的第 4 个元素）聚焦<br>示例：demo_mcxlab_srctype.m<br>源类型见这个表格下面的列表明：</td></tr><tr><td>cfg.{srcparam1,srcparam2}</td><td>1x4 向量，详见 cfg.srctype</td></tr><tr><td>cfg.srcpattern</td><td>详见 cfg.srctype</td></tr><tr><td>cfg.srcnum</td><td>同时模拟的源模式的数量； 仅适用于 'pattern' 源，有关详细信息，请参见 cfg.srctype='pattern'<br>示例 ：demo_photon_sharing.m</td></tr><tr><td>cfg.issrcfrom0</td><td>1-第一个体积元素是[0 0 0]，[0]-第一个体积元素是[1 1 1]</td></tr><tr><td>cfg.replaydet</td><td>仅在 cfg.outputtype 为“jacobian”、“wl”、“nscat”或“wp”且 cfg.seed 为数组时有效<br>-1：重放所有检测器并保存在单独的卷中（输出有 5 个维度）<br>0：重放所有检测器并将所有雅可比矩阵相加成一卷<br>正数：检测器重放和获取雅可比的索引</td></tr><tr><td>cfg.voidtime</td><td>对于宽场源，[1]-启动时启动计时器，或 0-进入第一个非零 体积元素时</td></tr></tbody></table>

- **源类型**
- 'pencil' 默认，铅笔束，不需要参数
- 'isotropic' - 各向同性源，不需要参数
- 'cone' - 均匀锥形光束，srcparam1(1) 是弧度的半角
- 'gaussian' \[\*\] - 准直的高斯光束，srcparam1(1) 指定腰部半径（以体素为单位）
- 'planar' \[\*\] - 一个 3D 四边形均匀平面源，三个角由 srcpos、srcpos+srcparam1(1:3) 和 srcpos+srcparam2(1:3) 指定
- 'pattern' \[\*\] - 一个 3D 四边形图案照明，
    
    - 同上，除了 srcparam1(4) 和 srcparam2(4) 指定图案阵列 x/y 维度，而 srcpattern 是浮点图案阵列，其值介于 \[ 0-1\]之间。
    
    - 如果 cfg.srcnum>1，srcpattern 必须是一个维度为 \[srcnum srcparam1(4) srcparam2(4)\] 的浮点数组
    - 示例：demo\_photon\_sharing.m
- 'pattern3d' \[\*\] - 3D 照明模式。 srcparam1{x,y,z} 定义维度，srcpattern 是一个浮点模式数组，值在 \[0-1\] 之间。
- 'fourier' \[\*\] - 空间频域源
    
    - 类似于 'planar'，除了 srcparam1(4) 和 srcparam2(4) 的整数部分代表 x/y 频率；
    - srcparam1(4) 的小数部分乘以2\*pi 表示相移 (phi0)；
    
    - 1.0 减去 srcparam2(4) 的小数部分是调制深度 (M)。代入方程：S=0.5_\[1+M_cos(2_pi_(fx_x+fy_y)+phi0)\], (0<=x,y,M<=1)
- 'arcsine' - 类似于各向同性，除了天顶角是均匀分布，而不是正弦分布。
- 'disk' \[\*\] - 指向 srcdir 的统一磁盘源；半径由 srcparam1(1) 设置（以网格为单位）
- 'fourierx' \[\*\] - 一个通用的傅里叶源，参数为 srcparam1: \[v1x,v1y,v1z,|v2|\], srcparam2: \[kx,ky,phi0,M\]
    - 归一化向量满足： srcdir cross v1=v2
    - 相移为 phi0_2_pi
- 'fourierx2d' \[\*\] - 一般二维傅里叶基准，参数 srcparam1: \[v1x,v1y,v1z,|v2|\], srcparam2: \[kx,ky,phix,phiy\]
    - 相移为 phi{x,y}_2_pi
- 'zgaussian' - 角度高斯光束，srcparam1(0) 指定天顶角 (zenith angle) 的方差
- 'line' - 线源，从线段之间发射
    - cfg.srcpos和cfg.srcpos+cfg.srcparam(1:3)，垂直方向均匀辐射
- 'slit' \[\*\] - 从线段之间发射的平行狭缝光束
    - cfg.srcpos 和cfg.srcpos+cfg.srcparam(1:3)，初始目录由 cfg.srcdir 指定
- 'pencilarray' - 一个矩形的铅笔光束阵列。
    - srcparam1 和 srcparam2 的定义类似于 'fourier'，
    - 除了 srcparam1(4) 和 srcparam2(4) 都是整数，分别表示 x/y 维度中的元素计数。

\== 输出控制 ==

<table><tbody><tr><td></td><td></td></tr><tr><td>cfg.issaveexit:</td><td>[0] - 保存检测到的光子的位置 (x,y,z) 和 (vx,vy,vz)<br>示例：demo_lambertian_exit_angle.m</td></tr><tr><td>cfg.issaveref:</td><td>[0] - 保存边界体素旁边的非零体素中的漫反射率/透射率。反射率数据存储为负值；必须在边界旁边填充零<br>示例：见底部的演示脚本</td></tr><tr><td>cfg.outputtype:</td><td>'flux' - 通量率，（默认值）<br>'fluence' - 在每个时间门上积分的流量，<br>“energy” - 每个体素的能量沉积<br>'jacobian' 或 'wl' - mua Jacobian（重播模式），<br>'nscat' 或 'wp' - 计算雅可比矩阵的加权散射计数（重播模式）<br><br>对于 jacobian/wl/wp 类型的例子：demo_mcxlab_replay.m 和 demo_replay_timedomain.m</td></tr><tr><td>cfg.session:</td><td>输出文件名的字符串（仅在没有返回变量时使用）</td></tr></tbody></table>

\== Debug ==

<table><tbody><tr><td></td><td></td></tr><tr><td>cfg.debuglevel</td><td>调试标志字符串，['R','M','P']之一或组合，无空格<br>'R'：调试RNG，输出fluence.data填充0-1个随机数<br>'M'：返回光子轨迹数据作为第 5 个输出<br>'P'：显示进度条</td></tr><tr><td>cfg.maxjumpdebug</td><td>[10000000|int] 当在输出中请求轨迹时，使用此参数设置存储的最大位置。 默认情况下，只存储前 1e6 个位置。</td></tr></tbody></table>

**带 \* 的字段为必填项； \[\] 中的选项是默认值**

Output:

fluence

<table><tbody><tr><td></td><td></td></tr><tr><td>fluence</td><td>一个struct数组，长度等于cfg的长度。<br>对于 fluence 的每个元素，fluence(i).data 是一个 4D 数组，其维度由 [size(vol) total-time-gates] 指定。<br>数组的内容是每个时间门的每个体积元素的归一化 fluence。</td></tr><tr><td>detphoton</td><td>（可选）一个结构体数组，长度等于 cfg 的长度。<br>从 v2018 开始，detphoton 包含以下子字段：<br>detphoton.detid：捕获光子的探测器的 ID(&gt;0)<br>detphoton.nscat：每种介质中的累积散射事件计数<br>detphoton.ppath：每种介质中的累积路径长度（部分路径长度） 需要将 cfg.unitinmm 与 ppath 相乘以将其转换为 mm。<br>detphoton.mom：每种介质中动量传递的累积 cos_theta<br>detphoton.p 或 .v：退出位置和方向，当 cfg.issaveexit=1 时<br>detphoton.w0：发射时的光子初始权重<br>detphoton.prop：光学特性，cfg.prop 的副本<br>detphoton.data：按顺序连接和转置的数组 [detid nscat ppath mom p v w0]'<br>“data”是 2018 年之前所有 mcxlab 中唯一的子字段</td></tr><tr><td>vol</td><td>（可选）一个结构体数组，每个元素都是对应于每个cfg实例的预处理卷。 每个卷都是一个 3D int32 数组。</td></tr><tr><td>seeds</td><td>（可选），如果给定，mcxlab 以字节数组 (uint8) 的形式返回每个检测到的光子的种子。 种子的列数等于 detphoton 的列数。</td></tr><tr><td>trajectory</td><td>（可选），如果给定，mcxlab 返回每个模拟光子的轨迹数据。 输出有6行，含义是<br>id: 1: 光子包的索引<br>pos: 2-4: 每个轨迹位置的x/y/z/<br>5：当前光子包权重<br>6：保留<br>默认情况下，mcxlab 只记录所有模拟光子的前 1e7 个位置； 更改 cfg.maxjumpdebug 以定义不同的限制。</td></tr></tbody></table>

例子

```
  
       % first query if you have supported GPU(s)
       info=mcxlab('gpuinfo')
 
       % define the simulation using a struct
       cfg.nphoton=1e7;
       cfg.vol=uint8(ones(60,60,60));
       cfg.vol(20:40,20:40,10:30)=2;    % add an inclusion
       cfg.prop=[0 0 1 1;0.005 1 0 1.37; 0.2 10 0.9 1.37]; % [mua,mus,g,n]
       cfg.issrcfrom0=1;
       cfg.srcpos=[30 30 1];
       cfg.srcdir=[0 0 1];
       cfg.detpos=[30 20 1 1;30 40 1 1;20 30 1 1;40 30 1 1];
       cfg.vol(:,:,1)=0;   % pad a layer of 0s to get diffuse reflectance
       cfg.issaveref=1;
       cfg.gpuid=1;
       cfg.autopilot=1;
       cfg.tstart=0;
       cfg.tend=5e-9;
       cfg.tstep=5e-10;
       % calculate the fluence distribution with the given config
       [fluence,detpt,vol,seeds,traj]=mcxlab(cfg);
 
       % integrate time-axis (4th dimension) to get CW solutions
       cwfluence=sum(fluence.data,4);  % fluence rate
       cwdref=sum(fluence.dref,4);     % diffuse reflectance
       % plot configuration and results
       subplot(231);
       mcxpreview(cfg);title('domain preview');
       subplot(232);
       imagesc(squeeze(log(cwfluence(:,30,:))));title('fluence at y=30');
       subplot(233);
       hist(detpt.ppath(:,1),50); title('partial path tissue#1');
       subplot(234);
       plot(squeeze(fluence.data(30,30,30,:)),'-o');title('TPSF at [30,30,30]');
       subplot(235);
       newtraj=mcxplotphotons(traj);title('photon trajectories')
       subplot(236);
       imagesc(squeeze(log(cwdref(:,:,1))));title('diffuse refle. at z=1');
```

剩下的机翻

此功能是 Monte Carlo eXtreme (MCX) URL 的一部分：http://mcx.space
