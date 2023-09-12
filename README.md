# Forking Tune Tagger
Forking Tune Tagger is a powerful command-line interface (CLI) tool designed to simplify the management and tagging of your music library. With this tool, you can effortlessly download songs and embed metadata, ensuring your music collection is organized and enriched with precision. Whether you're an audiophile looking to curate your collection or a music enthusiast who wants to keep everything neatly organized, Forking Tune Tagger has you covered.

## Features

- **Effortless Song Management**: Easily manage and organize your music collection with a few simple commands.

- **Precision Tagging**: Embed metadata, including song titles, artists, albums, and more, to ensure your music library is well-structured. If the metadata is not found on spotify, it embeds shazamed metadata, if shazam is unable to find it, it will embed metadata collected from YouTube.

- **User-Friendly CLI**: Just add your queries and run main.py

- **Other Media-Formats (Coming Soon)**: Want to download other media from YouTube, not just music? I'm working on adding this feature. Stay tuned for updates! In the meantime, you can configure your `media_type` in [media_config.txt](media_config_template.txt) for music downloads.


## Installation

To get started with Forking Tune Tagger, follow these steps:

1. Clone this repository to your local machine.
   ```bash
    https://github.com/sneakyshirtballs/Forking_Tune_Tagger.git
   ```
2. Configuration Settings For `media_config_template.txt`
- **Download_Path**: Specify the path where you want to save downloaded media files.
- **Media_Type**: Set the media type you want to download. For now, only "Music" is supported.
- **Resolution**: Specify the desired resolution (if applicable). For now, only "n/a" is supported.
- **Subtitles**: Indicate whether you want subtitles. For music, only "No" is supported.
- **Format**: Choose the desired media format. For music, only `m4a` is supported for now.
- **Queries**: List the YouTube *URLs* / *Search Query* / *Playlist* of the media you want to download. You can add multiple queries, some search terms, some links and/or playlists. **ONE** per line.

**Important**: Before using this template, make sure to follow these steps:
1. Rename [media_config_template.txt](media_config_template.txt) to `media_config.txt`.
2. Configure the settings in `media_config.txt` as described below.
3. Remove all other lines and keep the configurations only.

## Contributing
I'm open to any contribution to this repository, if anyone's interested, you can simply create a pull request providing your updated/suggested code and I will review and merge it as soon as possible.