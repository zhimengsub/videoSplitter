# videoSplitter

借助`ffmpeg`和`ffprobe`，把视频分为两半。

## 使用说明(exe)

1. 在[Releases](https://github.com/zhimengsub/videoSplitter/releases)中下载最新版本可执行文件

2. 把`videoSplitter.exe`与`ffmpeg.exe`、`ffprobe.exe`放入同一目录下（或将`ffmpeg.exe`、`ffprobe.exe`所在目录添加入PATH）

3. 把待处理视频拖放到`videoSplitter.exe`上即可，或使用命令行执行`videoSplitter.exe <视频文件路径>`

## 使用说明(py)

1. 安装[Python](https://www.python.org/downloads/)（注意3.9及以上版本不再支持win7）

1. 下载本仓库代码到本地

2. 把`videoSplitter.py`与`ffmpeg.exe`、`ffprobe.exe`放入同一目录下（或将`ffmpeg.exe`、`ffprobe.exe`所在目录添加入PATH）

3. 把待处理视频拖放到`videoSplitter.py`上即可，或使用命令行执行`python videoSplitter.py <视频文件路径>`
