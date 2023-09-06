from utils.custom_print import (p_status, p_success, p_terminate, p_warning)
from utils.common import (write_file_outtmpl)
from modules.common import yt_download_handler

def handle_music(configs):
    media_type, download_format, download_path = configs["Media_Type"], configs["Format"], configs["Download_Path"]

    p_status(f"Creating Download Options For {media_type}")
    
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

