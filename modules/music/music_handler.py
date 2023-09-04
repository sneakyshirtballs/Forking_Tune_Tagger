from utils.custom_print import (p_status, p_success, p_terminate, p_warning)

def handle_music(configs):
    media_type, download_format, queries = configs["Media_Type"], configs["Format"], configs["Queries"]