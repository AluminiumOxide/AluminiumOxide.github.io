---
title: "simple_run_cyclegan_in_custom_dataset"
date: "2022-03-31"
categories: 
  - "allophane"
  - "extracurricular"
---

[程序抢修](http://aluminium/allophane.com/index.php/2022/03/26/simple_rebulid_cyclegan/)和[数据集下载](http://aluminium/allophane.com/resource/SP_simulation2experiment.zip)懒的说了

首先在data/image\_folder.py的IMG\_EXTENSIONS里追加mat文件允许

```
IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
    '.tif', '.TIF', '.tiff', '.TIFF','.mat',
]
```

然后在data/unaligned\_dataset.py里的def \_\_getitem\_\_(self, index):里添加设置

```
    def __getitem__(self, index):
        """Return a data point and its metadata information.

        Parameters:
            index (int)      -- a random integer for data indexing

        Returns a dictionary that contains A, B, A_paths and B_paths
            A (tensor)       -- an image in the input domain
            B (tensor)       -- its corresponding image in the target domain
            A_paths (str)    -- image paths
            B_paths (str)    -- image paths
        """
        A_path = self.A_paths[index % self.A_size]  # make sure index is within then range
        if self.opt.serial_batches:   # make sure index is within then range
            index_B = index % self.B_size
        else:   # randomize the index for domain B to avoid fixed pairs.
            index_B = random.randint(0, self.B_size - 1)
        B_path = self.B_paths[index_B]

        # A_img = Image.open(A_path).convert('RGB')
        # B_img = Image.open(B_path).convert('RGB')
        A_data = load(A_path)
        A_data_float64 = A_data['pmn']
        A_data_float64 = A_data_float64 * 255
        A_data_float64 = np.reshape(A_data_float64, [256, 256, 1])
        A_data_float64 = np.concatenate((A_data_float64, A_data_float64, A_data_float64), axis=2)
        A_img = Image.fromarray(np.uint8(A_data_float64)).convert('RGB')
        B_data = load(B_path)
        B_data_float64 = B_data['psy']
        B_data_float64 = B_data_float64 * 255
        B_data_float64 = np.reshape(B_data_float64, [256, 256, 1])
        B_data_float64 = np.concatenate((B_data_float64, B_data_float64, B_data_float64), axis=2)
        B_img = Image.fromarray(np.uint8(B_data_float64)).convert('RGB')

        # apply image transformation
        A = self.transform_A(A_img)
        B = self.transform_B(B_img)

        return {'A': A, 'B': B, 'A_paths': A_path, 'B_paths': B_path}
```

也就是将

```
        A_img = Image.open(A_path).convert('RGB')
        B_img = Image.open(B_path).convert('RGB')
```

换成

```
        A_data = load(A_path)
        A_data_float64 = A_data['pmn']
        A_data_float64 = A_data_float64 * 255
        A_data_float64 = np.reshape(A_data_float64, [256, 256, 1])
        A_data_float64 = np.concatenate((A_data_float64, A_data_float64, A_data_float64), axis=2)
        A_img = Image.fromarray(np.uint8(A_data_float64)).convert('RGB')
        B_data = load(B_path)
        B_data_float64 = B_data['psy']
        B_data_float64 = B_data_float64 * 255
        B_data_float64 = np.reshape(B_data_float64, [256, 256, 1])
        B_data_float64 = np.concatenate((B_data_float64, B_data_float64, B_data_float64), axis=2)
        B_img = Image.fromarray(np.uint8(B_data_float64)).convert('RGB')
```

这里只是临时凑合一下，按理来说加上文件类型判断，保证原来的也能正常运行才好

```
        if A_path.split('.')[-1] == 'mat': # add img type judgement
            A_data = load(A_path)
            A_data_float64 = A_data['pmn']
            A_data_float64 = A_data_float64 * 255
            A_data_float64 = np.reshape(A_data_float64, [256, 256, 1])
            A_data_float64 = np.concatenate((A_data_float64, A_data_float64, A_data_float64), axis=2)
            A_img = Image.fromarray(np.uint8(A_data_float64)).convert('RGB')
            B_data = load(B_path)
            B_data_float64 = B_data['psy']
            B_data_float64 = B_data_float64 * 255
            B_data_float64 = np.reshape(B_data_float64, [256, 256, 1])
            B_data_float64 = np.concatenate((B_data_float64, B_data_float64, B_data_float64), axis=2)
            B_img = Image.fromarray(np.uint8(B_data_float64)).convert('RGB')
        else:
            A_img = Image.open(A_path).convert('RGB')
            B_img = Image.open(B_path).convert('RGB')
```

然后，在前面添加必要的库（其实也就是多了两个）

```
from scipy.io import loadmat as load
import numpy as np
```

记得先检查有没有下载

然后在命令行里运行

```
python train.py --dataroot ./datasets/SP_simulation2experiment --name SP_simulation2experiment_cyclegan --model cycle_gan --netG resnet_9blocks
```
