import re
from utils.custom_print import (p_status, p_terminate, p_warning)
from validators.media_config_validators import (
    validate_media_type,
    validate_resolution,
    validate_subtitles,
    validate_format,
    validate_queries,
)

def parse_config_file(file_path):
    pattern = r"Media_Type: (.+?)\nResolution: (.+?)\nSubtitles: (.+?)\nFormat: (.+?)\nQueries:\n([\s\S]+)"
    with open(file_path, 'r') as file:
        text = file.read()
    
    match = re.search(pattern, text)
    
    if match:
        media_type, resolution, subtitles, format, queries = match.groups()
        
        # Split the queries string into a list by lines
        queries = queries.strip().split('\n')
        
        if all([
            validate_media_type(media_type),
            validate_resolution(resolution),
            validate_subtitles(subtitles),
            validate_format(format),
            validate_queries(queries)
        ]):
            return [{
                "Media_Type": media_type,
                "Resolution": resolution,
                "Subtitles": subtitles,
                "Format": format,
                "Queries": queries
            }]
        else: p_terminate("media_config.txt has unsupported type/value!")
    
    else: p_terminate("media_config.txt is not formatted properly!")