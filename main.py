import colorama

from scripts.downloader import check_temp_files_exist, get_data_from_site
from scripts.extractor import get_data_from_archive
from scripts.finder_and_copier import find_and_copy_file
from variables import (DEFAULT_DOWNLOADED_FILES_PATH, DEFAULT_FILENAME, DEFAULT_ROOT_DIRECTORY, DEFAULT_URL,
                       DEFAULT_WEBDRIVER_PATH, DEFAULT_ZIP_FILENAME, F_RED)

colorama.init(autoreset=True)


def main():
    try:
        get_data_from_site(DEFAULT_URL)
        get_data_from_archive(DEFAULT_DOWNLOADED_FILES_PATH, DEFAULT_ZIP_FILENAME, DEFAULT_FILENAME)
        find_and_copy_file(DEFAULT_ROOT_DIRECTORY, DEFAULT_DOWNLOADED_FILES_PATH, DEFAULT_FILENAME)

        check_temp_files_exist(DEFAULT_DOWNLOADED_FILES_PATH)

    except FileNotFoundError:
        print(
            f'Пожалуйста проверьте данные:\n{F_RED}'
            f'\t{DEFAULT_ROOT_DIRECTORY=}\n'
            f'\t{DEFAULT_DOWNLOADED_FILES_PATH=}\n'
            f'\t{DEFAULT_WEBDRIVER_PATH=}\n'
            f'\t{DEFAULT_FILENAME=}\n'
            f'\t{DEFAULT_ZIP_FILENAME=}\n'
        )


if __name__ == '__main__':
    main()
