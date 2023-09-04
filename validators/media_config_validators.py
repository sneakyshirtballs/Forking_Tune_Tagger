# validators/validators.py

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
    return True # For Simplicity