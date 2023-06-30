import json
import os

import colorama

from scripts.downloader import Downloader
from scripts.extractor import Extractor
from scripts.file_finder import FileFinder
from utility import clearing_temp_files
from variables import (DEFAULT_DOWNLOAD_PATH, DEFAULT_FILENAME, DEFAULT_ROOT_PATH,
                       DEFAULT_URL, DEFAULT_WEBDRIVER_PATH, DEFAULT_ZIP_FILENAME, F_RED)

colorama.init(autoreset=True)


def check_metadata(filename='.\\meta.json'):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        with open(filename, 'w', encoding='utf-8') as file:
            template = {
                "title": "",
                "zip_filename": ""
            }
            json.dump(template, file, indent=4, ensure_ascii=False)


def main():
    downloader = Downloader()
    extractor = Extractor()
    finder = FileFinder()

    try:
        check_metadata()

        downloader.get_data_from_site()
        extractor.get_data_from_archive()
        finder.find_file()

    except FileNotFoundError:
        print(
            f'Пожалуйста проверьте данные:\n{F_RED}'
            f'\t{DEFAULT_ROOT_PATH=}\n'
            f'\t{DEFAULT_DOWNLOAD_PATH=}\n'
            f'\t{DEFAULT_WEBDRIVER_PATH=}\n'
            f'\t{DEFAULT_URL=}\n'
            f'\t{DEFAULT_FILENAME=}\n'
            f'\t{DEFAULT_ZIP_FILENAME=}\n'
        )

    finally:
        clearing_temp_files(DEFAULT_DOWNLOAD_PATH)


if __name__ == '__main__':
    main()
