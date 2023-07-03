import os
import zipfile

import colorama

from scripts.utility import Meta
from variables import F_BLUE, F_GREEN

colorama.init(autoreset=True)


class Extractor:
    def __init__(self, zip_path, zip_filename, dll_filename):
        self.zip_path = zip_path
        self.zip_filename = zip_filename
        self.dll_filename = dll_filename
        self.zip_fullpath = os.path.join(self.zip_path, self.zip_filename)

    def get_data_from_archive(self):
        print(f'Выбранный архив: {F_BLUE}{self.zip_filename}')
        print(f'Выбранный путь для извлечения: {F_GREEN}[{self.zip_path}]\n')
        if not os.path.exists(self.zip_fullpath):
            raise FileNotFoundError(f'Архив {self.zip_filename} не найден по указанному пути {self.zip_path}\n')

        with zipfile.ZipFile(f'{self.zip_fullpath}', 'r') as zipf:
            file_list = zipf.namelist()
            if self.dll_filename in file_list:
                zipf.extract(self.dll_filename, self.zip_path)
                print(f'Извлечено: {F_BLUE}{self.dll_filename}\n')
            else:
                print(f'Искомого файла нет\nСодержимое архива: {F_BLUE}{", ".join(file_list)}\n')
                raise FileNotFoundError(f'Файл {self.dll_filename} отсутствует в архиве {self.zip_filename}\n')


if __name__ == '__main__':
    meta = Meta()
    config = meta.create_metadata()
    extractor = Extractor(config['download_path'], config['zip_filename'], config['dll_filename'])
    extractor.get_data_from_archive()
