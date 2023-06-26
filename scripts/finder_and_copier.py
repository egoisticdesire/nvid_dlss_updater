import colorama
import os
import shutil

from variables import (DEFAULT_DOWNLOADED_FILES_PATH, DEFAULT_FILENAME, DEFAULT_ROOT_DIRECTORY, F_BLUE, F_YELLOW,
                       S_RESET)

colorama.init(autoreset=True)


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
            print('Старый файл заменен\n')


def main():
    find_and_copy_file(DEFAULT_ROOT_DIRECTORY, DEFAULT_DOWNLOADED_FILES_PATH, DEFAULT_FILENAME)


if __name__ == '__main__':
    main()
