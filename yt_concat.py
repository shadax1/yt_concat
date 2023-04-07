import os
from subprocess import check_output

script_path = os.path.dirname(os.path.abspath( __file__ ))
extension = "mp"

with open(f"{script_path}\links.txt", mode="rt", encoding="utf-8") as fp:
    count = 0
    with open(f"{script_path}\concat.txt", mode="wt", encoding="utf-8") as fp2:
        for line in fp.readlines():
            if "mp4" in line:
                extension = "mp4"
            elif "mp3" in line:
                extension = "mp3"
            else:
                lst_link = line.split()
                response = check_output(f"youtube-dl -g {lst_link[0]}", shell=True)
                output = response.decode("utf-8")
                lst_output = output.split("\n")
                if extension == "mp4":
                    os.system(fr'ffmpeg -ss {lst_link[1]} -i "{lst_output[0]}" -ss {lst_link[1]} -i "{lst_output[1]}" -t {lst_link[2]} -map 0:v -map 1:a -c:v libx264 -c:a aac {script_path}\{count}.{extension}')
                else:
                    os.system(fr'ffmpeg -ss {lst_link[1]} -t {lst_link[2]} -i "{lst_output[1]}" {script_path}\{count}.{extension}')
                fp2.write(f"file '{script_path}\{count}.{extension}'\n")
            count += 1
os.system(fr'ffmpeg -safe 0 -f concat -i {script_path}\concat.txt -c copy {script_path}\output.{extension}')