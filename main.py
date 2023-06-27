import colorama
import json
import os

from scripts.downloader import check_temp_files_exist, get_data_from_site
from scripts.extractor import get_data_from_archive
from scripts.finder_and_copier import FileFinder
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
    finder = FileFinder(DEFAULT_ROOT_PATH, DEFAULT_DOWNLOAD_PATH, DEFAULT_FILENAME)
    try:
        check_metadata()

        get_data_from_site(DEFAULT_URL)
        get_data_from_archive(DEFAULT_DOWNLOAD_PATH, DEFAULT_ZIP_FILENAME, DEFAULT_FILENAME)
        finder.find_file()

        check_temp_files_exist(DEFAULT_DOWNLOAD_PATH)

    except FileNotFoundError:
        print(
            f'Пожалуйста проверьте данные:\n{F_RED}'
            f'\t{DEFAULT_ROOT_PATH=}\n'
            f'\t{DEFAULT_DOWNLOAD_PATH=}\n'
            f'\t{DEFAULT_WEBDRIVER_PATH=}\n'
            f'\t{DEFAULT_FILENAME=}\n'
            f'\t{DEFAULT_ZIP_FILENAME=}\n'
        )


if __name__ == '__main__':
    main()
