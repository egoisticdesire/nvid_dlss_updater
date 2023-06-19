import os
import shutil
from colorama import init

from extractor import get_data_from_archive
from variables import (DEFAULT_DOWNLOADED_FILES_PATH, DEFAULT_FILENAME, DEFAULT_ROOT_DIRECTORY, DEFAULT_ZIP_FILENAME,
                       F_BLUE, F_RED, F_YELLOW, S_RESET)

init(autoreset=True)


def find_and_copy_file(root_directory, downloaded_files_directory, filename):
    file, extension = filename.split('.')
    copy_suffix = ' — копия'

    for root, dirs, files in os.walk(root_directory):
        if f'{file}.{extension}' in files:
            print(f'Файл {F_BLUE}{file}.{extension}{S_RESET} найден в каталоге {F_BLUE}{root}')

            original_file_path = os.path.join(root, f'{file}.{extension}')
            copy_file_path = os.path.join(root, f'{file}{copy_suffix}.{extension}')

            if not os.path.exists(f'{root}\\{file}{copy_suffix}.{extension}'):
                shutil.copy2(original_file_path, copy_file_path)
                print(f'Создана копия файла: {F_YELLOW}{copy_file_path}')

            replacement_file_path = os.path.join(downloaded_files_directory, f'{file}.{extension}')
            shutil.copy2(replacement_file_path, original_file_path)
            print(f'Старый файл заменен\n')


def main():
    try:
        get_data_from_archive(DEFAULT_DOWNLOADED_FILES_PATH, DEFAULT_ZIP_FILENAME, DEFAULT_FILENAME)
        find_and_copy_file(DEFAULT_ROOT_DIRECTORY, DEFAULT_DOWNLOADED_FILES_PATH, DEFAULT_FILENAME)
    except FileNotFoundError:
        print(
            f'Пожалуйста проверьте данные:\n{F_RED}'
            f'\t{DEFAULT_ROOT_DIRECTORY=}\n'
            f'\t{DEFAULT_DOWNLOADED_FILES_PATH=}\n'
            f'\t{DEFAULT_FILENAME=}\n'
            f'\t{DEFAULT_ZIP_FILENAME=}\n'
        )


if __name__ == '__main__':
    main()
