---
title: "ModernSignal_note2_wfdb"
date: "2022-10-20"
categories: 
  - "allophane"
  - "lesson"
---

Waveform Database

* * *

  
[python安装](https://physionet.org/content/wfdb-python/4.0.0/)直接 **pip install wfdb** 然后就没有然后了  
里面可能有用的就是这个示例，文档可以去[这里](https://wfdb.readthedocs.io/en/latest/wfdb.html)

```
# import the WFDB package
import wfdb

# load a record using the 'rdrecord' function
record = wfdb.rdrecord('sample-data/a103l')

# plot the record to screen
wfdb.plot_wfdb(record=record, title='Example signals')
```

* * *

[MATLAB安装](https://physionet.org/content/wfdb-matlab/0.10.0/)  
需要先安装[java](https://www.oracle.com/java/technologies/downloads/#jdk17-windows)  
这个可以在matlab命令行界面，直接选个风水比  
较好的目录(在matlab中)  
然后命令行运行

```
[old_path]=which('rdsamp'); if(~isempty(old_path)) rmpath(old_path(1:end-8)); end
wfdb_url='https://physionet.org/physiotools/matlab/wfdb-app-matlab/wfdb-app-toolbox-0-10-0.zip';
[filestr,status] = urlwrite(wfdb_url,'wfdb-app-toolbox-0-10-0.zip');
unzip('wfdb-app-toolbox-0-10-0.zip');
cd mcode
addpath(pwd)
savepath
```

当然，这等价于手动下载并解压 [压缩包](https://physionet.org/physiotools/matlab/wfdb-app-matlab/wfdb-app-toolbox-0-10-0.zip)  
把解压后下一层根目录添加到MATLAB的搜索路径里(主页/环境/设置路径)

好的现在可以在命令行  
wfdbdemo  
直接跑示例(注意这玩意会在上级刚才压缩包解压后的同级目录(不是子目录)下载示例数据，如果和之前数据集重复建议删除

[文档](https://physionet.org/physiotools/wag/wag.htm)可以查看这里**《注意眼睛！》**  
那么之后就可以开始充分的调用各种格式的数据了

* * *

**主要函数说明：**

**rdsamp** 读入生理信号及其注释

```
[signal,Fs,tm]=rdsamp(recordName,signaList,N,N0,rawUnits,highResolution)
```

举例：在Matlab中输入以下内容通过rdsamp函数可以读出MITDB信号库中的一个recordName为‘100‘的信号并借助plot函数显示：

```
 [tm, signal]=rdsamp('mitdb/100',[],1000);
plot(tm,signal(:,1));
```

其中,该信号中有两列采集信号，每列长为650000个采样点，所以获得的signal应该是一个2\*650000的矩阵。但是可以在函数输入可选项：

SignalList：选择其中某列信号读入，输入为空默认为全部列，此处就是默认全部；  
N：需要读入信号的长度，本身信号长为650000，此处只截取了其中1000长度；  
N0：截取信号开始的采样点，此处默认为1，也就是截取了信号的1–1000采样点；  
rawUnits：信号读入信号值需要的精度，具体请看帮助；  
highResolution：信号分辨率，1为高，0为低，默认为0

**rdann 读入注释信息**

```
[ann,type,subtype,chan,num,comments]=rdann(recordName,annotator,C,N,N0,type)
```

举例：

```
[tm, signal]=rdsamp('challenge/2013/set-a/a01');
[ann]=rdann('challenge/2013/set-a/a01','fqrs');
plot(tm,signal(:,1));hold on;grid on
plot(tm(ann),signal(ann,1),'ro','MarkerSize',4)
```

本程序首先用rdsamp函数读入‘challenge’信号库中的命名为‘a01’的全部信号，再用‘rdann’函数读入与之对应的注释信息，类型为‘fqrs’，也就是QRS出现的位置，最后由plot显示'Challenge’生理库中命名为‘a01’信号及其QRS注释信息  
其中红色的圆点就是注释文件中标注QRS出现的地方。其实注释信息我们可以通过一些算法求出来的，但是既然生理库中已经给出我们就可以直接用，而且他们官方的肯定经过矫正很准确的，既方便也有保证，直接拿来用何乐不为？另外如果我们想自己开发检测QRS或者R，可以将自己得到的结果和官方的注释信息对比，看看自己算法的准确率。

* * *

## **由于[官方文档主页](https://physionet.org/physiotools/wag/wag.htm)实在是太护眼了！直接搬运一下**

## Contents

### [Introduction](https://physionet.org/physiotools/wag/intro.htm)

### [FAQ](https://physionet.org/physiotools/wag/faq.htm)

### Applications

- [a2m, ad2m, ahaconvert, ahaecg2mit, m2a, md2a](https://www.physionet.org/physiotools/wag/a2m-1.htm): converting between AHA DB and WFDB formats
- [ann2rr, rr2ann](https://www.physionet.org/physiotools/wag/ann2rr-1.htm): convert annotation files to interval lists and vice versa
- [bxb](https://www.physionet.org/physiotools/wag/bxb-1.htm): ANSI/AAMI-standard beat-by-beat annotation comparator
- [calsig](https://www.physionet.org/physiotools/wag/calsig-1.htm): calibrate signals of a WFDB record
- [coherence](https://www.physionet.org/physiotools/wag/cohere-1.htm): estimate coherence and cross-spectrum of two time series
- [dfa](https://www.physionet.org/physiotools/wag/dfa-1.htm): detrended fluctuation analysis
- [ecgeval](https://www.physionet.org/physiotools/wag/ecgeva-1.htm): generate and run ECG analyzer evaluation script
- [ecgpuwave](https://www.physionet.org/physiotools/wag/ecgpuw-1.htm): QRS detector and waveform limit locator
- [edf2mit, mit2edf](https://www.physionet.org/physiotools/wag/edf2mi-1.htm): convert between EDF and WFDB-compatible formats
- [edr](https://www.physionet.org/physiotools/wag/edr-1.htm): derive a respiration signal from an ECG
- [epicmp](https://www.physionet.org/physiotools/wag/epicmp-1.htm): ANSI/AAMI-standard episode-by-episode annotation comparator
- [fft](https://www.physionet.org/physiotools/wag/fft-1.htm): fast Fourier transform
- [fir](https://www.physionet.org/physiotools/wag/fir-1.htm): general-purpose FIR filter for WFDB records
- [gqfuse](https://www.physionet.org/physiotools/wag/gqfuse-1.htm): combine QRS annotation files
- [gqrs, gqpost](https://www.physionet.org/physiotools/wag/gqrs-1.htm): QRS detector and post-processor
- [hrfft, hrlomb, hrmem](https://www.physionet.org/physiotools/wag/hrfft-1.htm): calculate and plot heart rate power spectra
- [hrstats](https://www.physionet.org/physiotools/wag/hrstat-1.htm): collect and summarize heart rate statistics from an annotation file
- [ihr](https://www.physionet.org/physiotools/wag/ihr-1.htm): calculate instantaneous heart rate
- [imageplt](https://www.physionet.org/physiotools/wag/imagep-1.htm): plot a greyscale image
- [log10](https://www.physionet.org/physiotools/wag/log10-1.htm): calculate common logarithms of two-column data
- [lomb](https://www.physionet.org/physiotools/wag/lomb-1.htm): estimate power spectrum using the Lomb periodogram method
- [lwcat](https://www.physionet.org/physiotools/wag/lwcat-1.htm): postprocess output of plt to make PostScript, EPS, PDF or PNG
- [memse](https://www.physionet.org/physiotools/wag/memse-1.htm): estimate power spectrum using maximum entropy (all poles) method
- [mfilt](https://www.physionet.org/physiotools/wag/mfilt-1.htm): general-purpose median filter for WFDB records
- [mrgann](https://www.physionet.org/physiotools/wag/mrgann-1.htm): merge annotation files
- [mxm](https://www.physionet.org/physiotools/wag/mxm-1.htm): ANSI/AAMI-standard measurement-by-measurement annotation comparator
- [nguess](https://www.physionet.org/physiotools/wag/nguess-1.htm): guess the times of missing normal beats in an annotation file
- [nst](https://www.physionet.org/physiotools/wag/nst-1.htm): noise stress test for ECG analysis programs
- [parsescp](https://www.physionet.org/physiotools/wag/parses-1.htm): parse SCP-ECG, optionally save in PhysioBank-compatible format
- [plot2d, plot3d](https://www.physionet.org/physiotools/wag/plot2d-1.htm): make 2-D or 3-D plots from text files of data, using **gnuplot**
- [plotstm](https://www.physionet.org/physiotools/wag/plotst-1.htm): produce scatter plot of ST measurement errors on a PostScript device
- [plt](https://www.physionet.org/physiotools/wag/plt-1.htm): make 2-D plots
- [pltf](https://www.physionet.org/physiotools/wag/pltf-1.htm): make function plots
- [pnnlist, pNNx](https://www.physionet.org/physiotools/wag/pnnlis-1.htm): derive pNNx statistics from an annotation interval list or an annotation file
- [pnwlogin](https://www.physionet.org/physiotools/wag/pnwlog-1.htm): provide direct access to PhysioNetWorks for WFDB applications
- [pschart](https://www.physionet.org/physiotools/wag/pschar-1.htm): produce annotated \`chart recordings' on a PostScript device
- [psfd](https://www.physionet.org/physiotools/wag/psfd-1.htm): produce annotated \`full-disclosure' plots on a PostScript device
- [rdann](https://www.physionet.org/physiotools/wag/rdann-1.htm): read a WFDB annotation file
- [rdedfann](https://www.physionet.org/physiotools/wag/rdedfa-1.htm): extract annotations from an EDF+ file
- [rdsamp](https://www.physionet.org/physiotools/wag/rdsamp-1.htm): read WFDB signal files
- [rxr](https://www.physionet.org/physiotools/wag/rxr-1.htm): ANSI/AAMI-standard run-by-run annotation comparator
- [sampfreq](https://www.physionet.org/physiotools/wag/sampfr-1.htm): show sampling frequency for a record
- [setwfdb, cshsetwfdb](https://www.physionet.org/physiotools/wag/setwfd-1.htm): set WFDB environment variables
- [sigamp](https://www.physionet.org/physiotools/wag/sigamp-1.htm): measure signal amplitudes of a WFDB record
- [sigavg](https://www.physionet.org/physiotools/wag/sigavg-1.htm): calculate averages of annotated waveforms
- [signame](https://www.physionet.org/physiotools/wag/signam-1.htm): print names of signals of a WFDB record
- [signum](https://www.physionet.org/physiotools/wag/signum-1.htm): print signal numbers of a WFDB record having specified names
- [skewedit](https://www.physionet.org/physiotools/wag/skewed-1.htm): edit skew fields of header file(s)
- [snip](https://www.physionet.org/physiotools/wag/snip-1.htm): copy an excerpt of a WFDB record
- [sortann](https://www.physionet.org/physiotools/wag/sortan-1.htm): rearrange annotations in canonical order
- [sqrs, sqrs125](https://www.physionet.org/physiotools/wag/sqrs-1.htm): single-channel QRS detector
- [stepdet](https://www.physionet.org/physiotools/wag/stepde-1.htm): single-channel step change detector
- [sumann](https://www.physionet.org/physiotools/wag/sumann-1.htm): summarize the contents of a WFDB annotation file
- [sumstats](https://www.physionet.org/physiotools/wag/sumsta-1.htm): derive aggregate statistics from bxb, rxr, etc., line-format output
- [tach](https://www.physionet.org/physiotools/wag/tach-1.htm): heart rate tachometer
- [time2sec](https://www.physionet.org/physiotools/wag/time2s-1.htm): convert WFDB standard time format into seconds
- [wabp](https://www.physionet.org/physiotools/wag/wabp-1.htm): arterial blood pressure (ABP) pulse detector
- [wav2mit, mit2wav](https://www.physionet.org/physiotools/wag/wav2mi-1.htm): convert between .wav and WFDB-compatible formats
- [wave](https://www.physionet.org/physiotools/wag/wave-1.htm): waveform analyzer, viewer, and editor
- [wfdb-config](https://www.physionet.org/physiotools/wag/wfdb-c-1.htm): print WFDB library version and configuration info
- [wfdb2mat](https://www.physionet.org/physiotools/wag/wfdb2m-1.htm): convert WFDB-compatible signal file to Matlab .mat file
- [wfdbcat](https://www.physionet.org/physiotools/wag/wfdbca-1.htm): copy WFDB files to standard output
- [wfdbcollate](https://www.physionet.org/physiotools/wag/wfdbco-1.htm): collate WFDB records into a multi-segment record
- [wfdbdesc](https://www.physionet.org/physiotools/wag/wfdbde-1.htm): read signal specifications
- [wfdbmap](https://www.physionet.org/physiotools/wag/wfdbma-1.htm): make a synoptic map of a WFDB record
- [wfdbtime](https://www.physionet.org/physiotools/wag/wfdbti-1.htm): convert time to sample number, elapsed, and absolute time
- [wfdbwhich](https://www.physionet.org/physiotools/wag/wfdbwh-1.htm): find a WFDB file and print its pathname
- [wqrs](https://www.physionet.org/physiotools/wag/wqrs-1.htm): single-channel QRS detector based on length transform
- [wrann](https://www.physionet.org/physiotools/wag/wrann-1.htm): write a WFDB annotation file
- [wrsamp](https://www.physionet.org/physiotools/wag/wrsamp-1.htm): write WFDB signal files
- [xform](https://www.physionet.org/physiotools/wag/xform-1.htm): sampling frequency, amplitude, and format conversion for WFDB records

### WFDB libraries

- [wfdb](https://www.physionet.org/physiotools/wag/wfdb-3.htm): Waveform Database library
- [wfdbf](https://www.physionet.org/physiotools/wag/wfdbf-3.htm): Waveform Database library wrappers for Fortran

### WFDB file formats

- [annot](https://www.physionet.org/physiotools/wag/annot-5.htm): WFDB annotation file formats
- [header](https://www.physionet.org/physiotools/wag/header-5.htm): WFDB header file format
- [signal](https://www.physionet.org/physiotools/wag/signal-5.htm): WFDB signal file formats
- [wfdbcal](https://www.physionet.org/physiotools/wag/wfdbca-5.htm): WFDB calibration file format

### Miscellaneous

- [xview](https://www.physionet.org/physiotools/wag/xview-7.htm): xview toolkit information

### Appendices

- _[Installing the WFDB Software Package](https://www.physionet.org/physiotools/wag/install.htm)_
- _[Evaluating ECG Analyzers](https://www.physionet.org/physiotools/wag/eval.htm)_
