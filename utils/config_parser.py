import re
from utils.custom_print import (p_status, p_terminate, p_warning)
from validators.media_config_validators import (
    validate_download_path,
    validate_media_type,
    validate_resolution,
    validate_subtitles,
    validate_queries,
    validate_format,
)

def parse_config_file(file_path):
    pattern = r"(?:Download_Path: (.+?)\n)?Media_Type: (.+?)\nResolution: (.+?)\nSubtitles: (.+?)\nFormat: (.+?)\nQueries:\n([\s\S]+)"

    with open(file_path, 'r') as file:
        text = file.read()
    
    match = re.search(pattern, text)
    
    if match:
        download_path, media_type, resolution, subtitles, download_format, queries = match.groups()

        # Split the queries string into a list by lines
        queries = queries.strip().split('\n')
        
        if all([
            validate_download_path(download_path),
            validate_media_type(media_type),
            validate_resolution(resolution),
            validate_subtitles(subtitles),
            validate_format(download_format),
            validate_queries(queries)
        ]):
            return {
                "Download_Path": download_path,
                "Media_Type": media_type,
                "Resolution": resolution,
                "Subtitles": subtitles,
                "Format": download_format,
                "Queries": queries
            }
        else: p_terminate("media_config.txt has unsupported type/value!")
    
    else: p_terminate("media_config.txt is not formatted properly!")