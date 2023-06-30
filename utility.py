import glob
import os


def clearing_temp_files(download_path):
    temp_file_pattern = '*.tmp'
    temp_files = glob.glob(os.path.join(download_path, temp_file_pattern))
    for temp_file in temp_files:
        os.remove(temp_file)
