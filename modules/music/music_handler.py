import os, requests
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

    yt_download_handler.handle_yt_download(configs, create_download_options)
    # await recognize_and_update_metadata(download_path, download_format) 



# Separate Function For Adding Metadata To Downloaded Music
async def recognize_and_update_metadata(directory_path, download_format):
    shazam = Shazam()
    
    for filename in os.listdir(directory_path):
        if filename.endswith(download_format):
            file_path = os.path.join(directory_path, filename)
            try:
                out = await shazam.recognize_song(file_path)
                if 'track' in out:
                    track_info = out['track']
                    audio = MP4(file_path)
                    audio['title'] = track_info['title']
                    audio['artist'] = track_info['subtitle']
                    
                    # Set the album name
                    audio['album'] = track_info['title']
                    
                    # Set album art if available
                    cover_art_url = track_info['images']['coverart']

                    cover_art_data = download_cover_art(cover_art_url)
                    if cover_art_data:
                        audio['covr'] = [MP4Cover(cover_art_data, MP4Cover.FORMAT_JPEG)]

                    audio.save()
                    p_success(f"Updated metadata for {filename}")
                else:
                    p_warning(f"Song recognition failed for {filename}")
            except Exception as e:
                p_terminate(f"Error processing {filename}: {str(e)}")

def download_cover_art(cover_art_url):
    # Download cover art image using requests
    try:
        response = requests.get(cover_art_url)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        p_terminate(f"Error downloading cover art: {str(e)}")
    return None