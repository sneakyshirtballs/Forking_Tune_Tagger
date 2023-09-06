import asyncio
from utils.config_parser import parse_config_file
from utils.custom_print import (p_status, p_terminate, p_warning, p_success)
from modules.music import music_handler

async def main():
    # Define the path to your configuration file
    file_path = "/home/hakuneko/Forking_Tune_Tagger_Test/media_config.txt"

    # Use the config_parser module to parse and validate the configuration file
    configs = parse_config_file(file_path)
    media_type = configs["Media_Type"]


    # Call appropriate functions based on media_type
    match media_type:
        case "Music":
            await music_handler.handle_music(configs)
        case _:
            p_terminate(f"{media_type} downloading is not available yet!")

    p_success("Forking Tune Tagger has *forked* its way to THE GOOD PLACE!")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())