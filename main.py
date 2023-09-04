from utils.config_parser import parse_config_file

# Define the path to your configuration file
file_path = "/home/hakuneko/Forking_Tune_Tagger_Test/media_config.txt"

# Use the config_parser module to parse and validate the configuration file
entries = parse_config_file(file_path)

print(entries)