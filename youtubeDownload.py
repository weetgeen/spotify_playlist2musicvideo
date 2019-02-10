import urllib.request
import os.path

from pytube import YouTube
from bs4 import BeautifulSoup




def find_video(track, playlistname, basefilepath):
#Search youtube for track based on artist and track name
    print('Searching youtube for: ' + track)
    textToSearch = track
    query = urllib.parse.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}, limit=1):  #select the first link of the search results
        videoURL = 'https://www.youtube.com' + vid['href']
        print(videoURL)
        check_if_video_exists(videoURL, playlistname, basefilepath)

def check_if_video_exists(videoURL, playlistname, basefilepath):
    #Checks if video is already present in basefilepath and skips download if so
    try:
        videoName = YouTube(videoURL).title
        if(os.path.isfile(basefilepath + playlistname + '\\' + videoName + '.mp4') == True):
            print('Video already exists, skipping download')
        else:
            try:
                download_video(videoURL, playlistname, basefilepath)
            except:
                print('HTTP Error, skipping download') #TODO create log of skipped videos and retry
                pass

    except:
        print('HTTP Error, skipping download')#TODO create log of skipped videos and retry
        pass


def download_video(videoURL, playlistname, basefilepath):
    #Download video
    print('Downloading.........')
    YouTube(videoURL).streams.first().download(basefilepath + playlistname)
    print('\n\n\n')

def create_playlist_folder(playlistname, basefilepath):
    #Create new folder of not existing
    if((os.path.isdir(basefilepath + playlistname)) == True):
        #Folder already exists, skip
        pass
    else:
        os.makedirs(basefilepath + playlistname) #make directory


