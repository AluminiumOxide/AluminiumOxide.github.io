---
title: "simple_python_libs_for_audio"
date: "2022-07-17"
categories: 
  - "allophane"
  - "extracurricular"
---

大概目前用到的音频转码相关的第三方库，按理来说一个pydub够用了，实在不行加个mutagen，其他的，，，再说

<table><tbody><tr><td>mutagen</td><td>一个添加音乐信息的库（但是会在部分情况下崩掉）</td></tr><tr><td>pydub</td><td>一个用于音频格式转换的库(用起来最暴力方便，但是部分情况有问题)</td></tr><tr><td>ffmpy3</td><td>一个基于调用ffmpeg而生的音频/视频处理库(非系统环境，没错我说的conda环境有问题，会定位不到系统的ffmpeg，而conda中的往往没有编码器)</td></tr><tr><td>eyed3</td><td>类似mutagen但是可以往mp3塞东西</td></tr></tbody></table>

## [mutagen](https://mutagen.readthedocs.io/en/latest/)

这东西只能说又爱又恨，这东西可以为flac文件添加几乎所有的标签，但是！！！它没办法直接给mp3加信息（恼）  
先在设置里把东西改成英文对应名称换就可以，比如

'title': \['标题'\],   
'encoder': \['编码人员'\],   
'conductor': \['指挥者'\],   
'composer': \['作曲者'\],   
'organization': \['发布者'\],   
'genre': \['流派'\],   
'description': \['备注'\],   
'tracknumber': \['13'\],   
'artist': \['参与创作的艺术家'\],   
'year': \['2000'\],   
'albumartist': \['唱片集艺术家'\],   
'album': \['唱片集'\]

用的最多的其实也就是《虽然有很多FLAC、MP3、ID3，但File是最泛用的》

```
from mutagen import File
```

然后实例化

```
audio = File(<音频文件目录的str>)
```

然后

```
audio["title"] = "只要是字符串就行"
audio["artist"] = "只要是字符串就行"
```

对于封面有些额外操作，毕竟得先打开文件

```
from mutagen.flac import Picture
# 然后
image = Picture()
with open(image_path, 'rb') as f:
   image.data = f.read()
f.close()
# 最后
audio.add_picture(image)
```

全干完了别忘了save()

```
audio.save()
```

## [pydub](https://github.com/jiaaro/pydub/blob/master/API.markdown)

PS:这个库居然没有readthedocs,直接去git下看文档

```
from pydub import AudioSegment
```

```
sound = AudioSegment.from_file(《文件路径str》, format=《文件类型str》)   # wav、mp3、ogg等
# 或者直接from_wav、from_ogg也都可以
```

可以直接在sound+《分贝 int》  
或者直接裁剪按毫秒为单位前5秒sound1\[:5000\]或后5秒sound1\[-5000:\]  
len(sound1)可以获得持续时间

此外在实例化sound的时候除了format还可以添加其他参数

- format str "wav"、“mp3”等
- sample\_width int 采样宽度 `1`对应 8bit音频；`2`对应16bit音频；`4`对应32bit音频；
- channels int 通道数 `1`单声道；`2`立体声
- frame\_rate int 采样率 44100；48000等
- start\_second int 从第几秒加载 默认是none
- duration int 加载多少秒 默认是none

就比如文档里的示例

```
sound = AudioSegment.from_file("/path/to/sound.raw", format="raw",
                                   frame_rate=44100, channels=2, sample_width=2)
```

导出的话就是使用export()方法,算了直接搬官方文档的示例

```
file_handle = sound.export("/path/to/output.mp3",
                           format="mp3",
                           bitrate="192k",
                           tags={"album": "The Bends", "artist": "Radiohead"},
                           cover="/path/to/albumcovers/radioheadthebends.jpg")
```

- format str "wav"、“mp3”等
- codec str 解码器按照描述ogg似乎需要这个"libvorbis"
- bitrate str 比特率"128k"等
- tags，{"album": "1989", "artist": "Taylor Swift"}参数同楼上的mutagen
- parameters 其他参数，例: `["-ac", "2"]` 参考[ffmpeg](https://www.ffmpeg.org/ffmpeg.html)
- id3v2\_version ？
- cover str 封面的路径

其他的看文档吧，反正我也用不到

## [ffmpy3](https://ffmpy3.readthedocs.io/en/latest/)

```
import ffmpy3
```

然后实例化并设置输入和输出的信息《反正就是调用ffmpeg》

```
ff = ffmpy3.FFmpeg(
    inputs={song_path: None},
    outputs={song_save_path+'.mp3': '-ar 48000 -ab 320k -f mp3'}
)
ff.run()
```

略了先，以后再补

## [eyed3](https://eyed3.readthedocs.io/en/latest/)

```
import eyed3
```

使用的时候先打开

```
audiofile = eyed3.load(song_save_path+'.mp3')
```

再添加标签

```
        audiofile.tag.artist = "artist"
        audiofile.tag.album = "album"
        audiofile.tag.album_artist = "album_artist"
        audiofile.tag.title = "title"
        audiofile.tag.images.set(3, open(《图像路径》, 'rb').read(), 'image/jpeg')
        audiofile.tag.track_num = str(这个是那个#的)
        audiofile.tag.encoder = "encoder"
        audiofile.tag.save()
```

略了先，以后再补
