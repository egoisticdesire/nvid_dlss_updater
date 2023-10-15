import os
import shutil

import colorama

from scripts.utility import Meta
from variables import F_BLUE, F_YELLOW, S_RESET

colorama.init(autoreset=True)


class FileFinder:
    def __init__(self, start_directory, download_path, dll_filename):
        self.start_directory = start_directory
        self.download_path = download_path
        self.dll_filename = dll_filename
        self.name, self.extension = dll_filename.split('.')
        self.copy_filename = f'{self.name} — копия.{self.extension}'

    def find_file(self):
        if not os.path.exists(self.start_directory):
            print(f'Выбранного каталога {F_BLUE}[{self.start_directory}]{S_RESET} не существует')
        for root, dirs, files in os.walk(self.start_directory):
            if self.dll_filename in files:
                print(f'Файл {F_BLUE}{self.dll_filename}{S_RESET} найден в каталоге {F_YELLOW}[{root}\\]')
                self._check_and_create_copy(root, self.dll_filename, self.copy_filename)
                self._replace_file(root, self.dll_filename)
        else:
            if not self.start_directory:
                print(
                    f'По указанному пути {F_BLUE}[{self.start_directory}]{S_RESET} '
                    f'не найдено ни одного файла {F_BLUE}{self.dll_filename}'
                )

    @staticmethod
    def _check_and_create_copy(root_path, orig_filename, copy_filename):
        copy_file_path = os.path.join(root_path, copy_filename)
        orig_file_path = os.path.join(root_path, orig_filename)
        if not os.path.exists(copy_file_path):
            shutil.copy2(orig_file_path, copy_file_path)
            print(f'Создана копия файла: {F_YELLOW}[{copy_file_path}]')

    def _replace_file(self, root_path, filename):
        orig_file_path = os.path.join(root_path, filename)
        replacement_file_path = os.path.join(self.download_path, filename)
        shutil.copy2(replacement_file_path, orig_file_path)
        print('Старый файл заменен\n')


if __name__ == '__main__':
    meta = Meta()
    config = meta.create_metadata()
    finder = FileFinder(config['root_path'], config['download_path'], config['dll_filename'])
    finder.find_file()
