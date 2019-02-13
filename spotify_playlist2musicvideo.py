import sys
import spotipy
import spotipy.util as util
import os
import youtubeDownload
from random import randint
from time import sleep
from json.decoder import JSONDecodeError

#Spotify developer settings; create a free account on developer.spotify.com
os.environ["SPOTIPY_CLIENT_ID"]     = ''
os.environ["SPOTIPY_CLIENT_SECRET"] = ''
os.environ["SPOTIPY_REDIRECT_URI"]  = ''
username = '' #spotify username


#Root of filepath in which folders are created to store playlists video's
basefilepath = ""

scope    = 'user-library-read'


songs = [] #declare empty list to store songs in

def show_tracks(results, playlistname):
    for i, item in enumerate(results['items']):
        track = item['track']
        songs.append(track['artists'][0]['name'] +' '+ track['name'])
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))



def download_all_playlist():    
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

		download()
                
	else:
		print("Can't get token for", username)

		
def download_single_playlist(playlist_id, playlistname):
    sp = spotipy.Spotify(auth=token)
    results = sp.user_playlist(username, playlist_id, fields="tracks,next")
    tracks = results['tracks']

    #Create new folder of not existing
    youtubeDownload.create_playlist_folder(playlistname, basefilepath)
    
    show_tracks(tracks, playlistname)
    while tracks['next']:
	    tracks = sp.next(tracks)
	    show_tracks(tracks, playlistname)

    download()


#TODO add progress bar
def download():
    for song in songs:
        youtubeDownload.find_video(song , playlistname, basefilepath)
        

#TODO Access token expires for long downloads
try:
    token = util.prompt_for_user_token(username)
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)


print('Provide playlist URI or type ALL to download all your playlists')
playlist_id = input()

if(playlist_id == 'ALL'):
	print('Downloading all playlists')
	download_all_playlist()
else:
        playlist_id = playlistURI.split("playlist:",1)[1]    #Takes the playlist number of the spotifyURI
	#TODO verify user input
	print('Playlist name')
	playlistURI = input() #TODO get playlist name from spotify
	
	download_single_playlist(playlist_id, playlistname)	
