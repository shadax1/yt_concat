# yt_concat
Python script that concatenates segments of YouTube and Twitch videos together in either mp3 or mp4 format.
It currently supports YouTube links (both mp3 and mp4), Twitch videos (both mp3 and mp4) and Twitch clips (only mp4).

## Requirements
+ Python 3
+ `ffmpeg` which can be downloaded [here](https://github.com/BtbN/FFmpeg-Builds/releases). Type `ffmpeg` in a command line to see if the command is found or not
+ `yt-dlp` which can be downloaded [here](https://github.com/yt-dlp/yt-dlp/releases). Type `yt-dlp` in a command line to see if the command is found or not

This script used to use `youtube-dl` but it hasn't been maintained since December 2021 so `yt-dlp` is a good alternative.

## How to use
1. Download this repository and unzip it anywhere on your disk.

2. Open `links.txt` and add either `mp3` or `mp4` in the first line based on the type of file you want.

3. In the next lines, add links, timestamp and duration separated by comas or the line can contain only a link for the entirety of the video/audio stream:

    >`<youtube/twitch link>`, `<timestamp>`, `<duration of the clip from that timestamp>`

    >`<youtube/twitch link>`

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
    https://clips.twitch.tv/EntertainingCrackyDinosaurJebaited-B3L3T7XGxBsEU8rE
    ```
    This will concatenate all these clips together into a single `mp4` file. Notice how you can mix YouTube and Twitch links together.

    ### Note regarding mixing links together
    I have mainly done tests with links coming from the same channel but it's also possible to mix different video links from various channels. The main thing to take into account if that's what you want to do with the `mp4` tag in particular, then the videos' maximum resolutions should be the same or it will likely result in errors. Same goes for `mp3` as it can sometimes result in distorted audio.

4. Finally, open a command line and type:
    ```
    python yt_concat.py
    ```

    The resulting file will be named `output_X.mp3` or `output_X.mp4` where X is an incrementing number in case other outputs exist in the folder. The script also saves each segment in the `segments` folder but deletes them at each runtime.
