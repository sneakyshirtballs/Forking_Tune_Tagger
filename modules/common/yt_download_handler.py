import yt_dlp
from utils.custom_print import (p_status, p_terminate)
from utils.common import update_download_history

def handle_yt_download(configs, create_download_options):
    queries, media_type = configs["Queries"], configs["Media_Type"]

    # Updates previous download history
    download_path, download_format = configs["Download_Path"], configs["Format"]
    update_download_history(download_path, download_format)
    
    p_status(f"Downloading {media_type} - Total {len(queries)} Queries")

    for url in queries:
        download_options = create_download_options()

        # here after downloading, send the file info in
        # recognize_and_update_metadata type function to
        # update the metadata of the file, also send the thumbnails
        # title, channel name, channel icon as parameters
        # if the recognize... func fails to update its metadata, use
        # the title, channel name thumbnails as title, artist, cover in mutagen
        with yt_dlp.YoutubeDL(download_options) as ydl:
            try:
                ydl.download(url)
            except yt_dlp.utils.DownloadError as e:
                p_terminate(f"{str(e)}")
                

    p_status(f"Finished Downloading {media_type}")