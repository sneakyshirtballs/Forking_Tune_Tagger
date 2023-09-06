import os
from utils.custom_print import p_terminate, p_status, p_warning
from utils.common import lookup_yt_vid, get_videos_from_playlist

# Function to validate download path
def validate_download_path(path):
    # Check if the specified path exists
    if not os.path.exists(path):
        p_terminate(f"The specified path '{path}' does not exist.")
    
    # Check if 'media_config.txt' exists in the specified path
    media_config_path = os.path.join(path, 'media_config.txt')
    if not os.path.isfile(media_config_path):
        p_terminate("The 'media_config.txt' file is not available in the specified path.")
    
    # If both checks pass, return True
    return True

# Function to validate media type
def validate_media_type(value):
    valid_types = ["Music"]  # Add more valid types as needed
    return value in valid_types

# Function to validate format
def validate_format(value):
    valid_formats = ["m4a"]  # Add more valid formats as needed
    return value in valid_formats

# Function to validate resolution
def validate_resolution(value):
    valid_resolutions = ["n/a"] # If resolution is n/a, consider it valid
    return value in valid_resolutions

# Function to validate subtitles
def validate_subtitles(value):
    valid_subtitles = ["Yes", "No"]  # Add more valid values as needed
    return value in valid_subtitles

# Function to validate queries
def validate_queries(queries):
    validated_queries = []  # Store validated queries here

    for query in queries:
        # Check if its a channel link
        if "/channel/" in query:
            p_warning(f"Skipping Query, Channel Link Detected: {query}")
            continue
        
        # Check if its a Playlist, if so, extend validated_queries with it
        if "/playlist?list=" in query:
            p_warning(f"Playlist link detected: {query}")
            choice = input("Do you want to download this playlist? (yes/no): ").strip().lower()
            if choice == "yes":
                # Get individual video links from the playlist
                video_links = get_videos_from_playlist(query)
                validated_queries.extend(video_links)
                continue
            else:
                p_status("Playlist skipped.")
                continue
        
        # If the interpreter comes here, it means It's a valid video link or search term
        video_info = lookup_yt_vid(query)
        video_link = f"https://www.youtube.com/watch?v={video_info['video_id']}"
        validated_queries.append(video_link)
        continue


    return validated_queries