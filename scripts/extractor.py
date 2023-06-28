import os
import zipfile

import colorama

from variables import (DEFAULT_DOWNLOAD_PATH, DEFAULT_FILENAME, DEFAULT_ZIP_FILENAME, F_BLUE, F_GREEN)

colorama.init(autoreset=True)


class Extractor:
    def __init__(self, zip_path, zip_filename, filename):
        self.zip_path = zip_path
        self.zip_filename = zip_filename
        self.filename = filename
        self.zip_fullpath = os.path.join(self.zip_path, self.zip_filename)

    def get_data_from_archive(self):
        print(f'Выбранный архив: {F_BLUE}{self.zip_filename}')
        print(f'Выбранный путь для извлечения: {F_GREEN}{self.zip_path}\n')
        if not os.path.exists(self.zip_fullpath):
            raise FileNotFoundError(f'Архив {self.zip_filename} не найден по указанному пути {self.zip_path}\n')

        with zipfile.ZipFile(f'{self.zip_fullpath}', 'r') as zipf:
            file_list = zipf.namelist()
            if self.filename in file_list:
                zipf.extract(self.filename, self.zip_path)
                print(f'Извлечено: {F_BLUE}{self.filename}\n')
            else:
                print(f'Искомого файла нет\nСодержимое архива: {F_BLUE}{", ".join(file_list)}\n')
                raise FileNotFoundError(f'Файл {self.filename} отсутствует в архиве {self.zip_filename}\n')


if __name__ == '__main__':
    extractor = Extractor(DEFAULT_DOWNLOAD_PATH, DEFAULT_ZIP_FILENAME, DEFAULT_FILENAME)
    extractor.get_data_from_archive()
