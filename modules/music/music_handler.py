import os, spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from mutagen.mp4 import MP4, MP4Cover
from shazamio import Shazam
from utils.custom_print import ( p_success, p_warning)
from utils.common import (write_file_outtmpl, download_thumbnail)
from modules.common import yt_download_handler

# Load environment variables from .env file
load_dotenv()
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

async def handle_music(configs):
    download_format, download_path = configs["Format"], configs["Download_Path"]
    
    def create_download_options():
        download_options = {
        'format': 'bestaudio/best',
        'outtmpl': write_file_outtmpl(download_path, download_format),
        'download_archive': f"{download_path}/.download_history.txt",
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': download_format,
        'preferredquality': '320',
        }],
        }
        
        return download_options

    await yt_download_handler.handle_yt_download(configs, create_download_options, detect_music_and_embed_metadata)


async def detect_music_and_embed_metadata(file_info):
    shazam= Shazam() # initialize shazam

    file_path = file_info['file_path'] 
    yt_title, yt_channel_name, yt_thumbnail = (file_info['title'], file_info['channel_name'], file_info['thumbnail'])
    
    yt_track_info = {
                "title": yt_title,
                "album": f"YouTube: {yt_channel_name}",
                "artist": yt_channel_name,
                "thumbnail": download_thumbnail(yt_thumbnail),
            }

    try:
        shazam_output = await shazam.recognize_song(file_path)
        if "track" in shazam_output:
            p_success(f"Successfully Shazamed {file_path}")

            shazamed_artist = shazam_output["track"]["subtitle"]
            shazamed_track_title = shazam_output["track"]["title"]
            shazam_track_info = {
                "title": shazamed_track_title,
                "album": f"Shazam: {shazamed_artist}",
                "artist": shazamed_artist,
                "thumbnail": download_thumbnail(shazam_output["track"]["images"]["coverart"])
            }
            
            # Initialize Spotipy with the credentials
            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
            try:
                # Fetch track details
                spotify_track_results = sp.search(q=f"track:{shazamed_track_title} artist:{shazamed_artist}",
                                                  type='track', limit=1)

                if spotify_track_results and 'tracks' in spotify_track_results and 'items' in spotify_track_results['tracks'] and len(spotify_track_results['tracks']['items']) > 0:
                    spotify_track_info = spotify_track_results['tracks']['items'][0]
                    #Extract desired information
                    spotify_title = spotify_track_info['name']
                    spotify_album = spotify_track_info['album']['name']
                    spotify_artist_name = spotify_track_info['artists'][0]['name']
                    spotify_cover_art = spotify_track_info['album']['images'][0]['url']

                    spotify_track_info =  {
                    'title': spotify_title,
                    'album': spotify_album,
                    'artist': spotify_artist_name,
                    'thumbnail': download_thumbnail(spotify_cover_art),
                    }
                    p_success(f"Found Metadata From Spotify {file_path}")
                    embed_with_mutagen(spotify_track_info, file_path)
                
                else:
                    p_warning(f"Metadata Not Available On Spotify: {file_path}")
                    p_warning(f"Embedding Shazamed Metadata Instead!")
                    embed_with_mutagen(shazam_track_info, file_path)

            except Exception as e:
                p_warning(f"Metadata Not Found On Spotify: {file_path} {str(e)}")
                p_warning(f"Embedding Shazamed Metadata Instead!")
                embed_with_mutagen(shazam_track_info, file_path)

        else:
            p_warning(f"Unable To Detect Song With Shazam: {file_path}")
            p_warning(f"Embedding YouTube Metadata Instead!")
            embed_with_mutagen(yt_track_info, file_path)

    except Exception as e:
        p_warning(f"FAILED To Detect Song With Shazam: {file_path} {str(e)}")
        p_warning(f"Embedding YouTube Metadata Instead!")
        embed_with_mutagen(yt_track_info, file_path)

# Helper Function to Embed Metadata With Mutagen
def embed_with_mutagen(track_info, file_path):
    audio = MP4(file_path)

    audio['\xa9nam'] = track_info['title']
    audio['\xa9ART'] = track_info['artist']    
    audio['\xa9alb'] = track_info['album']

    if track_info["thumbnail"]:
        audio['covr'] = [MP4Cover(track_info["thumbnail"], MP4Cover.FORMAT_JPEG)]

    audio.save()
    p_success(f"Embedded Metadata: {file_path}")