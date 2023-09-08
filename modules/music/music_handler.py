import os, requests, mutagen
from mutagen.mp4 import MP4, MP4Cover
from shazamio import Shazam
from utils.custom_print import (p_status, p_success, p_terminate, p_warning)
from utils.common import (write_file_outtmpl)
from modules.common import yt_download_handler

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

    file_path, download_format = (file_info['file_path'], file_info['download_format'])    
    yt_title, yt_channel_name, yt_thumbnail = (file_info['title'], file_info['channel_name'], file_info['thumbnail'])

    try:
        out = await shazam.recognize_song(file_path)
        if "track" in out:
            print(out)
        else:
            p_warning(f"Unable To Detect Song With Shazam: {file_path} {str(e)}")
            p_warning(f"Embedding YouTube Metadata Instead!")

            track_info = {
                "title": yt_title,
                "artist": yt_channel_name,
                "thumbnail": yt_thumbnail,
                "album": yt_title
            }
            embed_with_mutagen(track_info)

    except Exception as e:
        p_warning(f"FAILED To Detect Song With Shazam: {file_path} {str(e)}")
        p_warning(f"Embedding YouTube Metadata Instead!")

        track_info = {
            "title": yt_title,
            "artist": yt_channel_name,
            "thumbnail": yt_thumbnail,
            "album": yt_title
        }
        embed_with_mutagen(track_info)

# Helper Function
def embed_with_mutagen(track_info):
    m4a_file_path = "/home/hakuneko/Downloads/Detected Music/{48} {Alec Benjamin - Must Have Been The Wind (Lyrics)} {o9EBm4-9isI}.m4a"

    # Open the M4A file using mutagen
    audio = mutagen.File(m4a_file_path)
    if audio:
        # Extract artist, title, and album
        artist = audio.get('artist', [''])[0]
        title = audio.get('title', [''])[0]
        album = audio.get('album', [''])[0]

        # Extract other metadata if needed
        duration = audio.info.length  # Duration in seconds
        bitrate = audio.info.bitrate  # Bitrate in bits per second

        # Print the extracted metadata
        print(f"Artist: {artist}")
        print(f"Title: {title}")
        print(f"Album: {album}")
        print(f"Duration: {duration} seconds")
        print(f"Bitrate: {bitrate} bps")
    else:
        print("Invalid M4A file.")


# Separate Function For Adding Metadata To Downloaded Music
# async def recognize_and_update_metadata(directory_path, download_format):
#     shazam = Shazam()
    
#     for filename in os.listdir(directory_path):
#         if filename.endswith(download_format):
#             file_path = os.path.join(directory_path, filename)
#             try:
#                 out = await shazam.recognize_song(file_path)
#                 if 'track' in out:
#                     track_info = out['track']
#                     audio = MP4(file_path)
#                     audio['title'] = track_info['title']
#                     audio['artist'] = track_info['subtitle']
                    
#                     # Set the album name
#                     audio['album'] = track_info['title']
                    
#                     # Set album art if available
#                     cover_art_url = track_info['images']['coverart']

#                     cover_art_data = download_cover_art(cover_art_url)
#                     if cover_art_data:
#                         audio['covr'] = [MP4Cover(cover_art_data, MP4Cover.FORMAT_JPEG)]

#                     audio.save()
#                     p_success(f"Updated metadata for {filename}")
#                 else:
#                     p_warning(f"Song recognition failed for {filename}")
#             except Exception as e:
#                 p_terminate(f"Error processing {filename}: {str(e)}")

# def download_cover_art(cover_art_url):
#     # Download cover art image using requests
#     try:
#         response = requests.get(cover_art_url)
#         if response.status_code == 200:
#             return response.content
#     except Exception as e:
#         p_terminate(f"Error downloading cover art: {str(e)}")
#     return None