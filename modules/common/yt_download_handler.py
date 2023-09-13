import yt_dlp, os, requests, re, json
from bs4 import BeautifulSoup
from utils.custom_print import (p_status, p_terminate, p_warning)
from utils.common import update_download_history

async def handle_yt_download(configs, create_download_options, embed_metadata):
    queries, media_type = configs["Queries"], configs["Media_Type"]

    # Updates previous download history
    download_path, download_format = configs["Download_Path"], configs["Format"]
    update_download_history(download_path, download_format)
    
    p_status(f"Downloading {media_type} - Total {len(queries)} Queries")

    for url in queries:
        download_options = create_download_options()

        with yt_dlp.YoutubeDL(download_options) as ydl:
            try:
                info = ydl.extract_info(url, download=False)  # Extract video info without downloading

                # Check if info_dict is None or if the video has already been recorded in the archive
                if info is None or info.get('archive'):
                    continue  # Skip processing for this video

                file_path = ydl.prepare_filename(info)  # Get the file path
                base_path, old_extension = os.path.splitext(file_path)
                # Fix file path with actual download_format (file_extension)
                file_path = f"{base_path}.{download_format}"   
                
                ydl.download([url])  # Download the video

                # Create a dictionary to encapsulate all the information
                file_info = {
                    'file_path': file_path,
                    'title': info.get('title', 'Unknown Title'),
                    'channel_name': info.get('uploader', 'Unknown Channel'),
                    'thumbnail': get_channel_icon_url(info.get("channel_url"), info.get("thumbnail")),
                }
                await embed_metadata(file_info)

            except yt_dlp.utils.DownloadError as e:
                p_terminate(f"{str(e)}")
    
    p_status(f"Finished Downloading {media_type}")


# Helper Function
def get_channel_icon_url(channel_url, thumbnail_url):
    channel_url = channel_url + "/about"
    try:
        soup = BeautifulSoup(requests.get(channel_url, cookies=({'CONSENT': 'YES+1'})).text, "html.parser")
        data = re.search(r"var ytInitialData = ({.*});", str(soup.prettify())).group(1)
        json_data = json.loads(data)
        original_channel_logo = json_data['header']['c4TabbedHeaderRenderer']['avatar']['thumbnails'][2]['url']

        hi_res_channel_logo = re.sub(r'=s\d+-', f'=s{1024}-', original_channel_logo)
        return hi_res_channel_logo
        
    except Exception as e:
        p_warning(f"Error Fetching Channel Icon URL: {str(e)}")
        p_warning("Will Use Thumbnail as Cover Art")
        return thumbnail_url