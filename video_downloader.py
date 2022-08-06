from pytube import YouTube
import os

#=========VARIABLES==============#
use_custom_destination = False
PATH = "C:/Users/HP/Desktop/music"
#If this is True, audio will be downloaded to provided PATH.
#If False, audio will be downloaded to a 'music' folder, same location of python script
#================================#

URL = input("Input the video URL: ")

def progress_function(stream, chunk, bytes_remaining):
    current_download = (audio.filesize - bytes_remaining)
    total_download = audio.filesize
    percentage = round((current_download*100)/total_download,1)
    print(str(current_download) + "/" + str(total_download) + "      " + str(percentage) + "%", end='\r', flush=True)
    #This function is executed every time a video chunk is downloaded, and gives us a scuffed progress bar

video = YouTube(URL, on_progress_callback=progress_function)
#Youtube class, also responsible for calling the progress function

length_minutes, length_seconds = divmod(video.length, 60)
#Converts length from pure seconds to mm:ss format

print("\nVideo: " + video.title)
print("By: " + video.author)
print("Length: " + str(length_minutes) + ":" + str(length_seconds))
formatted_views = f"{video.views:,}"
print("Views: " + formatted_views)
#Gives us video info

audio = video.streams.get_audio_only()
#Chooses audio-only stream with highest quality

print("\nDownloading...")

if use_custom_destination:
    downloaded_audio = audio.download(output_path=PATH)
else:
    downloaded_audio = audio.download(".\music")
#See first comment


name, extension = os.path.splitext(downloaded_audio)
new_audio = name + ".mp3"
os.rename(downloaded_audio, new_audio)
#Even though the download is audio-only, it's still downloaded as MP4. This turns it into MP3.

input("\nDownload Successful")

