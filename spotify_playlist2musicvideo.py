import sys
import spotipy
import spotipy.util as util
import os
import youtubeDownload
from random import randint
from time import sleep
from json.decoder import JSONDecodeError

#Een test comment


#Spotify developer settings; create a free account on developer.spotify.com
os.environ["SPOTIPY_CLIENT_ID"]     = '919bc08b499a419d864bbf1574fb07cf'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'c393f03e11a441c9865b9111434e6c01'
os.environ["SPOTIPY_REDIRECT_URI"]  = 'https://hp-iot.nl/index.php'
username = 'weetgeen'  #spotify username


#Root of filepath in which folders are created to store playlists video's
basefilepath = "D:\Projects\Python\spotifyMusicVideo\VIDEOS\\"

scope    = 'user-library-read'


def show_tracks(results, playlistname):
    for i, item in enumerate(results['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))

        youtubeDownload.find_video(track['artists'][0]['name'] + ' ' + track['name'], playlistname, basefilepath)      

try:
    token = util.prompt_for_user_token(username)
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

    
if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print()
            print(playlist['name'])

            #Create new folder of not existing
            youtubeDownload.create_playlist_folder(playlist['name'], basefilepath)
            
            print('  total tracks', playlist['tracks']['total'])
            results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
            tracks = results['tracks']
            show_tracks(tracks, playlist['name'])
            while tracks['next']:
                tracks = sp.next(tracks)
                show_tracks(tracks, playlist['name'])
                
else:
    print("Can't get token for", username)
