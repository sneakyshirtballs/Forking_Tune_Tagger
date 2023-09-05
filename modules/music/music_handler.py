from utils.custom_print import (p_status, p_success, p_terminate, p_warning)
from utils.common import (create_download_options)

def handle_music(configs):
    media_type, download_format, queries = configs["Media_Type"], configs["Format"], configs["Queries"]
    download_path = configs["Download_Path"]

    p_status(f"Creating Download Options For {media_type}")
    download_options = create_download_options(media_type, download_format, download_path)