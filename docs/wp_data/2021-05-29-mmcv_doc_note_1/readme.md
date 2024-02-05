---
title: "MMCV_doc_note_1"
date: "2021-05-29"
categories: 
  - "prohibite"
---

## File IO

两个通用API，用于加载和转储不同格式的文件

### 1\. 加载和转储数据

当前支持的格式为json，yaml和pickle

```
import mmcv

# load data from a file
data = mmcv.load('test.json')
data = mmcv.load('test.yaml')
data = mmcv.load('test.pkl')
# load data from a file-like object
with open('test.json', 'r') as f:
    data = mmcv.load(f, file_format='json')

# dump data to a string
json_str = mmcv.dump(data, file_format='json')

# dump data to a file with a filename (infer format from file extension)
mmcv.dump(data, 'out.pkl')

# dump data to a file with a file-like object
with open('test.yaml', 'w') as f:
    data = mmcv.dump(data, f, file_format='yaml')
```

扩展api以支持更多文件格式也非常方便。编写一个从`**BaseFileHandler**` 继承的文件处理程序，并以一种或几种文件格式注册它。

您至少需要实现3种方法。

```
import mmcv

# To register multiple file formats, a list can be used as the argument. 如果你需要注册多个，那就设置成列表，比如['txt', 'log']
# @mmcv.register_handler(['txt', 'log'])
@mmcv.register_handler('txt')
class TxtHandler1(mmcv.BaseFileHandler):  

    def load_from_fileobj(self, file):
        return file.read()

    def dump_to_fileobj(self, obj, file):
        file.write(str(obj))

    def dump_to_str(self, obj, **kwargs):
        return str(obj)
```

以`PickleHandler`为示例，分别定义load和dump（也就是至少搞几个加载和保存的示例）

```
import pickle

class PickleHandler(mmcv.BaseFileHandler):

    def load_from_fileobj(self, file, **kwargs):
        return pickle.load(file, **kwargs)

    def load_from_path(self, filepath, **kwargs):
        return super(PickleHandler, self).load_from_path(
            filepath, mode='rb', **kwargs)

    def dump_to_str(self, obj, **kwargs):
        kwargs.setdefault('protocol', 2)
        return pickle.dumps(obj, **kwargs)

    def dump_to_fileobj(self, obj, file, **kwargs):
        kwargs.setdefault('protocol', 2)
        pickle.dump(obj, file, **kwargs)

    def dump_to_path(self, obj, filepath, **kwargs):
        super(PickleHandler, self).dump_to_path(
            obj, filepath, mode='wb', **kwargs)
```

### 2.加载文本文件作为列表或字典

例如`a.txt`，一个具有5行的文本文件。

```
a
b
c
d
e
```

然后使用`list_from_file`从a.txt加载列表。

```
>>> mmcv.list_from_file('a.txt')
['a', 'b', 'c', 'd', 'e']
>>> mmcv.list_from_file('a.txt', offset=2)
['c', 'd', 'e']
>>> mmcv.list_from_file('a.txt', max_num=2)
['a', 'b']
>>> mmcv.list_from_file('a.txt', prefix='/mnt/')
['/mnt/a', '/mnt/b', '/mnt/c', '/mnt/d', '/mnt/e']
```

例如`b.txt`，一个具有3行的文本文件。

```
1 cat
2 dog cow
3 panda
```

然后使用`dict_from_file`从a.txt加载列表。（）

```
>>> mmcv.dict_from_file('b.txt')
{'1': 'cat', '2': ['dog', 'cow'], '3': 'panda'}
>>> mmcv.dict_from_file('b.txt', key_type=int)
{1: 'cat', 2: ['dog', 'cow'], 3: 'panda'}
```

## Image

该模块提供了一些图像处理方法，需要`opencv`库。

### 1\. 读/写/显示

要读取或写入图像文件，请使用`imread`或`imwrite`。

```
import mmcv

img = mmcv.imread('test.jpg')
img = mmcv.imread('test.jpg', flag='grayscale')
img_ = mmcv.imread(img) # nothing will happen, img_ = img
mmcv.imwrite(img, 'out.jpg')
```

从字节读取图像

```
with open('test.jpg', 'rb') as f:
    data = f.read()
img = mmcv.imfrombytes(data)
```

显示图像文件或加载的图像

```
mmcv.imshow('tests/data/color.jpg')
# this is equivalent to

for i in range(10):
    img = np.random.randint(256, size=(100, 100, 3), dtype=np.uint8)
    mmcv.imshow(img, win_name='test image', wait_time=200)
```

显示图像文件或加载的图像

### 2\. 色彩空间转换

支持的转换方法：

- bgr2gray
- grey2bgr
- bgr2rgb
- rgb2bgr
- bgr2hsv
- hsv2bgr

```
img = mmcv.imread('tests/data/color.jpg')
img1 = mmcv.bgr2rgb(img)
img2 = mmcv.rgb2gray(img1)
img3 = mmcv.bgr2hsv(img)
```

### 3\. 调整大小

有三种调整大小的方法。所有`imresize_*`方法都有一个参数`return_scale`，如果这个参数是`False`，那么返回值仅仅是调整大小的图像，否则是一个元组。`(resized_img, scale)`

```
# resize to a given size
mmcv.imresize(img, (1000, 600), return_scale=True)

# resize to the same size of another image
mmcv.imresize_like(img, dst_img, return_scale=False)

# resize by a ratio
mmcv.imrescale(img, 0.5)

# resize so that the max edge no longer than 1000, short edge no longer than 800
# without changing the aspect ratio
mmcv.imrescale(img, (1000, 800))
```

### 4\. 旋转

## 旋转[](https://mmcv.readthedocs.io/en/latest/image.html#rotate)

要将图像旋转某个角度，请使用`imrotate`。可以指定中心，默认为原图的中心。旋转的方式有两种，一种是保持图片大小不变，旋转后图片的某些部分会被裁剪掉，另一种是扩大图片大小以适应旋转后的图片。

```
img = mmcv.imread('tests/data/color.jpg')

# rotate the image clockwise by 30 degrees.
img_ = mmcv.imrotate(img, 30)

# rotate the image counterclockwise by 90 degrees.
img_ = mmcv.imrotate(img, -90)

# rotate the image clockwise by 30 degrees, and rescale it by 1.5x at the same time.
img_ = mmcv.imrotate(img, 30, scale=1.5)

# rotate the image clockwise by 30 degrees, with (100, 100) as the center.
img_ = mmcv.imrotate(img, 30, center=(100, 100))

# rotate the image clockwise by 30 degrees, and extend the image size.
img_ = mmcv.imrotate(img, 30, auto_bound=True)
```

### 翻动

要翻转图像，请使用`imflip`。

```
img = mmcv.imread('tests/data/color.jpg')

# flip the image horizontally
mmcv.imflip(img)

# flip the image vertically
mmcv.imflip(img, direction='vertical')
```

## 裁剪

`imcrop` 可以用一个或一些区域裁剪图像，表示为 (x1, y1, x2, y2)。

```
import mmcv
import numpy as np

img = mmcv.imread('tests/data/color.jpg')

# crop the region (10, 10, 100, 120)
bboxes = np.array([10, 10, 100, 120])
patch = mmcv.imcrop(img, bboxes)

# crop two regions (10, 10, 100, 120) and (0, 0, 50, 50)
bboxes = np.array([[10, 10, 100, 120], [0, 0, 50, 50]])
patches = mmcv.imcrop(img, bboxes)

# crop two regions, and rescale the patches by 1.2x
patches = mmcv.imcrop(img, bboxes, scale_ratio=1.2)
```

## 填充

有两种方法`impad`和`impad_to_multiple`垫的图像与给定的值的特定大小。

```
img = mmcv.imread('tests/data/color.jpg')

# pad the image to (1000, 1200) with all zeros
img_ = mmcv.impad(img, shape=(1000, 1200), pad_val=0)

# pad the image to (1000, 1200) with different values for three channels.
img_ = mmcv.impad(img, shape=(1000, 1200), pad_val=[100, 50, 200])

# pad the image on left, right, top, bottom borders with all zeros
img_ = mmcv.impad(img, padding=(10, 20, 30, 40), pad_val=0)

# pad the image on left, right, top, bottom borders with different values
# for three channels.
img_ = mmcv.impad(img, padding=(10, 20, 30, 40), pad_val=[100, 50, 200])

# pad an image so that each edge is a multiple of some value.
img_ = mmcv.impad_to_multiple(img, 32)
```
