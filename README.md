# yt_concat
Python script that concatenates segments of YouTube videos together in either `mp3` or `mp4` format.

## Requirements
+ Python 3
+ `ffmpeg` which can be downloaded from [here](https://github.com/BtbN/FFmpeg-Builds/releases). The script assumes `ffmpeg` is in the `PATH` environment variables. Type `ffmpeg` in a command line to see if the command is found or not
+ `yt-dlp` which can be downloaded from [here](https://github.com/yt-dlp/yt-dlp/releases). The script assumes `yt-dlp` is in the `PATH` environment variables. Type `yt-dlp` in a command line to see if the command is found or not

This script used to use `youtube-dl` but it hasn't been maintained since December 2021 so `yt-dlp` is a good alternative.

## How to use
Download this repository and unzip it anywhere on your disk.

Open `links.txt` and add either `mp3` or `mp4` in the first line based on the type of file you want.

Then, the next lines will each contain: youtube link, timestamp, duration of the clip from that timestamp
Here is an example:
```
mp4
https://www.youtube.com/watch?v=EhKXCrV2eJw 4:18 0:18
```
This means you will get an 18 second `mp4` clip starting from the 4:18 timestamp in the video. You can also use decimals to be more precise.

Here is another example with multiple entries:
```
mp4
https://www.youtube.com/watch?v=EhKXCrV2eJw 0:02.5 0:02.5
https://www.youtube.com/watch?v=EhKXCrV2eJw 0:53.7 0:06
https://www.youtube.com/watch?v=EhKXCrV2eJw 1:19.5 0:20
https://www.youtube.com/watch?v=EhKXCrV2eJw 4:18 0:18
https://www.youtube.com/watch?v=EhKXCrV2eJw 4:44 0:09
https://www.youtube.com/watch?v=EhKXCrV2eJw 5:50 0:21
```
This will concatenate all these clips together into a single `mp4` file.

**Note:** when using `mp4`, don't mix different video resolutions or it won't work.

Finally, open a command line and type:
```
python yt_concat.py
```

The resulting file will be named `output.mp3` or `output.mp4`. The script also saves each segment.
