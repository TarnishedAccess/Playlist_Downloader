from pytube import YouTube
from pytube import Playlist
from pytube.exceptions import VideoUnavailable
from slugify import slugify
import os
import time

#=========VARIABLES==============#
use_custom_destination = True
PATH = "C:/Users/HP/Desktop/music/"
#If this is True, audio will be downloaded to provided PATH.
#If False, audio will be downloaded to a 'music' folder, same location of python script
#================================#

URL = input("Please input the playlist URL.")

playlist = Playlist(URL)
#Playlist class

print("\nUpdating playlist " + playlist.title + " by " + playlist.owner + "\n")

start_time = time.mktime(time.localtime())
#We use this at the end to find out how long the execution took.

playlist_video_number = playlist.length
playlist_scanned_video_number = 0
#Use these variables to see how many videos are left

downloaded_videos = 0
#We use this variable later to see how many videos were downloaded

for link in playlist.video_urls:
    try:
        video = YouTube(link, use_oauth=True, allow_oauth_cache=True)
    except VideoUnavailable:
        downloaded_videos = downloaded_videos + 1
        pass
    else:
        playlist_scanned_video_number = playlist_scanned_video_number + 1
        print(str(playlist_video_number - playlist_scanned_video_number) + " videos remaining")
        #Look two comments ago

        file_name = slugify(video.title) + ".mp3"
        #We slugify to make sure the names are valid file names

        if use_custom_destination:
            folder_path = PATH
        else:
            folder_path = "./music/"
        #See first comment

        #print(folder_path + file_name)
        #Show folder/file for debugging purposes

        if not os.path.exists(folder_path + file_name):
        #If the file doesn't already exist...       

            length_minutes, length_seconds = divmod(video.length, 60)
            #Converts length from pure seconds to mm:ss format

            print("Video: " + video.title)
            print("By: " + video.author)
            print("Length: " + str(length_minutes) + ":" + str(length_seconds))
            formatted_views = f"{video.views:,}"
            print("Views: " + formatted_views)
            #Gives us video info

            audio = video.streams.get_audio_only()
            #Chooses audio-only stream with highest quality

            print("Downloading...\n")

            if use_custom_destination:
                downloaded_audio = audio.download(output_path=PATH, filename = slugify(video.title))
            else:
                downloaded_audio = audio.download(".\music", filename = slugify(video.title))
            #See first comment

            name, extension = os.path.splitext(downloaded_audio)
            new_audio = name + ".mp3"
            os.rename(downloaded_audio, new_audio)
            #Even though the download is audio-only, it's still downloaded as MP4. This turns it into MP3.

            downloaded_videos = downloaded_videos + 1
            #increment downloaded videos counter

finish_time = time.mktime(time.localtime())
#We use this to find out how long the execution took

minutes, seconds = divmod(finish_time - start_time, 60)

print(str(playlist_video_number - playlist_scanned_video_number) + " videos unavailable")
input("Playlist Download Complete. \n" + str(downloaded_videos) + " New videos downloaded taking " + str(int(minutes)) + ":" + str(int(seconds)))