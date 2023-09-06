from utils.custom_print import (p_status, p_success, p_terminate, p_warning)
from utils.common import update_download_history

def handle_yt_download(configs, create_download_options):
    queries, media_type = configs["Queries"], configs["Media_Type"]

    # Updates previous download history
    download_path, download_format = configs["Download_Path"], configs["Format"]
    update_download_history(download_path, download_format)
    
    p_status(f"Downloading {media_type} - Total {len(queries)} Queries")

    p_status(queries)

    p_status(f"Finished Downloading {media_type}")