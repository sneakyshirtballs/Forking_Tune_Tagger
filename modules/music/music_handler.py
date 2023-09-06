from utils.custom_print import (p_status, p_success, p_terminate, p_warning)
from utils.common import (write_file_outtmpl)
from modules.common import yt_download_handler

def handle_music(configs):
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

