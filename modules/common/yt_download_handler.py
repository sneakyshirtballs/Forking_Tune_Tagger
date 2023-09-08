import yt_dlp
from utils.custom_print import (p_status, p_terminate)
from utils.common import update_download_history

def handle_yt_download(configs, create_download_options, embed_metadata):
    queries, media_type = configs["Queries"], configs["Media_Type"]

    # Updates previous download history
    download_path, download_format = configs["Download_Path"], configs["Format"]
    update_download_history(download_path, download_format)
    
    p_status(f"Downloading {media_type} - Total {len(queries)} Queries")

    for url in queries:
        download_options = create_download_options()

        with yt_dlp.YoutubeDL(download_options) as ydl:
            try:
                info = ydl.extract_info(url, download=False)  # Extract video info without downloading

                # Check if info_dict is None or if the video has already been recorded in the archive
                if info is None or info.get('archive'):
                    continue  # Skip processing for this video

                file_path = ydl.prepare_filename(info)  # Get the file path
                ydl.download([url])  # Download the video

                # Create a dictionary to encapsulate all the information
                file_info = {
                    'file_path': file_path,
                    'title': info.get('title', 'Unknown Title'),
                    'channel_name': info.get('uploader', 'Unknown Channel'),
                    'thumbnail': info.get('thumbnail')
                }

                embed_metadata(file_info)

            except yt_dlp.utils.DownloadError as e:
                p_terminate(f"{str(e)}")
    
    p_status(f"Finished Downloading {media_type}")