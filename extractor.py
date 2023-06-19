import time
import zipfile
import rarfile
import py7zr
from colorama import init
from variables import (DEFAULT_DOWNLOADED_FILES_PATH, DEFAULT_FILENAME, DEFAULT_ZIP_FILENAME, F_BLUE, F_GREEN)

init(autoreset=True)


def get_data_from_archive(zip_path, zip_filename, filename):
    print(f'Выбранный архив: {F_BLUE}{zip_filename}')
    print(f'Выбранный путь для извлечения: {F_GREEN}{zip_path}\n')
    time.sleep(3)
    with zipfile.ZipFile(f'{zip_path + zip_filename}', 'r') as zipf:
        file_list = zipf.namelist()
        if filename in file_list:
            zipf.extract(filename, zip_path)
            print(f'Извлечено: {F_BLUE}{filename}\n')
            time.sleep(2)
        else:
            print(f'Искомого файла нет\nСодержимое архива: {F_BLUE}{", ".join(file_list)}\n')
            raise FileNotFoundError(f'Файл {filename} отсутствует в архиве {zip_filename}\n')


def main():
    get_data_from_archive(DEFAULT_DOWNLOADED_FILES_PATH, DEFAULT_ZIP_FILENAME, DEFAULT_FILENAME)


if __name__ == '__main__':
    main()
