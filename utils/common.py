import re, os, yt_dlp
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


# Update Download History based on certain conditions. (mostly used in yt_download_handler)
def update_download_history(download_path, download_format):
    # Create the path to the download history text file
    download_history_txt_path = os.path.join(download_path, '.download_history.txt')
    
    # Check if the download path contains files with the specified download format extension
    detected_files = [file for file in os.listdir(download_path) if file.endswith(download_format)]
    
    if not detected_files:
        p_warning(f"No files with '{download_format}' extension found in the download path.")
    
    # Check if the download history text file exists
    if os.path.exists(download_history_txt_path):
        # Read the content of the download history text file
        with open(download_history_txt_path, 'r') as history_file:
            download_links = [line.strip() for line in history_file.readlines()]
        
        # Check if the number of download links matches the number of matching files
        if len(download_links) != len(detected_files):
            p_terminate("Mismatch between the number of download links and the number of detected files.")
            
            # handling the mismatch
        else:
            p_success("Download history is up to date.")    
    else:
        p_warning("No previous download history found!")
    
    # Additional logic can be added here as needed.


def lookup_yt_vid(query):
    try:
        ydl_opts = {
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(query, download=False)
            
            if 'entries' in info_dict:
                video_info = info_dict['entries'][0]
                # Extract relevant metadata including channel name
                return {
                    "title": video_info.get('title', ''),
                    "thumbnail_url": video_info.get('thumbnail', ''),
                    "video_id": video_info.get('id', ''),
                    "channel_name": video_info.get('channel', ''),
                    # Add more metadata fields as needed
                }
            else:
                p_terminate(f"No YouTube video found for query: {query}")
    except Exception as e:
        p_terminate(f"Error while looking up YouTube video: {str(e)}")