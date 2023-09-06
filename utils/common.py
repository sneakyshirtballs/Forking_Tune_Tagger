import re, os
from utils.custom_print import (p_status, p_success, p_terminate, p_warning)

def write_file_outtmpl(download_path, download_format):
    unique_id = create_next_unique_id(download_path, download_format)

    unique_id = "{" + str(unique_id) + "}"
    title = "{%(title)s}"
    video_id = "{%(id)s}"
    ext = "%(ext)s"

    template = f"{download_path}/{unique_id} {title} {video_id}.{ext}"
    
    return template

# Generates the next unique ID for a file based on the existing files in the directory.
def create_next_unique_id(download_path, download_format):
    existing_ids = []

    for file_name in os.listdir(download_path):
        if file_name.endswith(f".{download_format}"):
            result = extract_file_info(file_name)
            unique_id = result['unique_id']
            existing_ids.append(unique_id)

    next_id = max(existing_ids) + 1 if existing_ids else 0

    return next_id

# Extracts the file information (unique ID, title, and video ID) from a given file name.
def extract_file_info(file_name):
    pattern = r'\{(.*?)\}' # Matches text inside curly braces
    matches = re.findall(pattern, file_name)

    if len(matches) == 3:
        unique_id = int(matches[0])
        title = matches[1]
        video_id = matches[2]
        return {
            'unique_id': unique_id,
            'title': title,
            'video_id': video_id
        }
    else:
        p_terminate(f"file naming is inconsistent: {file_name}")