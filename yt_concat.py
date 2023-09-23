import os
from subprocess import check_output

script_dir = os.path.dirname(__file__)

def main():
    extension = ""
    count = 1
    with open(f"{script_dir}{os.path.sep}links.txt", mode="rt", encoding="utf-8") as fp_links:
        with open(f"{script_dir}{os.path.sep}concat.txt", mode="wt", encoding="utf-8") as fp_concat:
            for line in fp_links.readlines():
                #first line
                if "mp4" in line:
                    extension = "mp4"
                    print("[SCRIPT] format is mp4")
                elif "mp3" in line:
                    extension = "mp3"
                    print("[SCRIPT] format is mp3")

                #after the first line
                else:
                    if len(line.split()) == 3: #when a timestamp and duration is specified
                        link = line.split()[0]
                        timestamp = line.split()[1]
                        length = line.split()[2]

                        #get stream
                        response = check_output(f"yt-dlp -g {link} --no-warnings", shell=True)
                        url = response.decode("utf-8")
                        video_stream = url.split("\n")[0] #youtube separates both audio and video
                        audio_stream = url.split("\n")[1] #youtube separates both audio and video

                        if extension == "mp4":
                            if "youtu" in link: #youtube link
                                get_yt_segment(extension, timestamp, length, video_stream, audio_stream, count)
                                fp_concat.write(f"file '{script_dir}{os.path.sep}segments{os.path.sep}{count}.{extension}'\n")
                            elif "twitch" in link: #twitch link
                                get_twitch_segment(extension, timestamp, length, url, count)
                                fp_concat.write(f"file '{script_dir}{os.path.sep}segments{os.path.sep}{count}.{extension}'\n")
                            else:
                                print(f"[WARNING] link {link} is unsupported")
                        else:
                            if "youtu" in link: #youtube link
                                get_yt_segment(extension, timestamp, length, video_stream, audio_stream, count)
                                fp_concat.write(f"file '{script_dir}{os.path.sep}segments{os.path.sep}{count}.{extension}'\n")
                            elif "twitch" in link: #twitch link
                                if "clip" not in link:
                                    get_twitch_segment(extension, timestamp, length, url, count)
                                    fp_concat.write(f"file '{script_dir}{os.path.sep}segments{os.path.sep}{count}.{extension}'\n")
                                else:
                                    print(f"[WARNING] can't extract an audio segment from a twitch clip... --> {link}")
                            else:
                                print(f"[WARNING] link {link} is unsupported")
                    
                    elif len(line.split()) == 1: #no timestamp/duration specified -> download the whole thing
                        link = line
                        get_full(extension, link, count)
                        fp_concat.write(f"file '{script_dir}{os.path.sep}segments{os.path.sep}{count}.{extension}'\n")
                    else:
                        print(f"[WARNING] information missing in line --> {line}")
                    count += 1

    print("[INFO] concatenating all segments...")
    if not os.path.exists(f"{script_dir}{os.path.sep}output.{extension}"):
        final_file_name = f"{script_dir}{os.path.sep}output.{extension}"
    else:
        bool_saved = False
        count_filename = 1
        while not bool_saved:
            if os.path.exists(f"{script_dir}{os.path.sep}output_{count_filename}.{extension}"):
                count_filename += 1
            else:
                final_file_name = f"{script_dir}{os.path.sep}output_{count_filename}.{extension}"
                bool_saved = True
    os.system(fr'ffmpeg -safe 0 -f concat -i "{script_dir}{os.path.sep}concat.txt" -c copy {final_file_name} -loglevel error -stats')
    print(fr"[INFO] concatenated file saved under '{final_file_name}'")

#FFMPEG - YT-DLP
def get_yt_segment(extension, timestamp, length, video_stream, audio_stream, count):
    print(f"[SCRIPT] entry {count} is a youtube segment")
    if extension == "mp4":
        os.system(fr'ffmpeg -ss "{timestamp}" -i "{video_stream}" -ss "{timestamp}" -i "{audio_stream}" -t "{length}" -map 0:v -map 1:a -c:v libx264 -c:a aac "{script_dir}{os.path.sep}segments{os.path.sep}{count}.{extension}" -loglevel error -stats')
    elif extension == "mp3":
        os.system(fr'ffmpeg -ss "{timestamp}" -t "{length}" -i "{audio_stream}" "{script_dir}{os.path.sep}segments{os.path.sep}{count}.{extension}" -loglevel error -stats')

def get_twitch_segment(extension, timestamp, length, url, count):
    print(f"[SCRIPT] entry {count} is a twitch segment")
    if extension == "mp4":
        os.system(fr'ffmpeg -ss "{timestamp}" -i "{url[:-1]}" -t "{length}" "{script_dir}{os.path.sep}segments{os.path.sep}{count}.{extension}" -loglevel error -stats') #url[:-1] to remove the \n
    elif extension == "mp3":
        os.system(fr'ffmpeg -ss "{timestamp}" -i "{url[:-1]}" -t "{length}" -map 0:a "{script_dir}{os.path.sep}segments{os.path.sep}{count}.{extension}" -loglevel error -stats') #url[:-1] to remove the \n

def get_full(extension, link, count):
    if extension == "mp4":
        if "youtu" in link: #youtube link
            print(f"[SCRIPT] entry {count} is a full youtube video")
        elif "twitch" in link: #twitch link
            if "clip" not in link:
                print(f"[SCRIPT] entry {count} is a full twitch video")
            else:
                print(f"[SCRIPT] entry {count} is a twitch clip")
        os.system(fr'yt-dlp --output "{script_dir}{os.path.sep}segments{os.path.sep}{count}.{extension}" -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" --quiet --progress {link}')
    
    elif extension == "mp3":
        if "clip" in link: #condition only to display the following message
            print(f"[INFO] can't extract mp3 from a twitch clip... --> {link}")
        else:
            if "youtu" in link: #youtube link
                print(f"[SCRIPT] entry {count} is a full youtube audio")
            elif "twitch" in link and "clip" not in link: #twitch link
                print(f"[SCRIPT] entry {count} is a full twitch audio")
            os.system(fr'yt-dlp --output "{script_dir}{os.path.sep}segments{os.path.sep}{count}.{extension}" -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 --quiet --progress {link}')
    else:
        print(f"[WARNING] link {link} is unsupported")

def empty_segments_folder():
    path = fr'{script_dir}{os.path.sep}segments'
    for f in os.listdir(path):
        os.remove(fr"{path}{os.path.sep}{f}")

empty_segments_folder()
main()
