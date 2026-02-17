import os

def get_file_path(directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return os.path.join(directory, filename)