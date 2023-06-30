import os
import shutil

import colorama

from variables import (DEFAULT_DOWNLOAD_PATH, DEFAULT_FILENAME, DEFAULT_ROOT_PATH, F_BLUE, F_YELLOW, S_RESET)

colorama.init(autoreset=True)


class FileFinder:
    def __init__(
        self,
        start_directory=DEFAULT_ROOT_PATH,
        download_path=DEFAULT_DOWNLOAD_PATH,
        filename=DEFAULT_FILENAME
    ):
        self.start_directory = start_directory
        self.download_path = download_path
        self.filename = filename
        self.name, self.extension = filename.split('.')
        self.copy_filename = f'{self.name} — копия.{self.extension}'

    def find_file(self):
        for root, dirs, files in os.walk(self.start_directory):
            if self.filename in files:
                print(f'Файл {F_BLUE}{self.filename}{S_RESET} найден в каталоге {F_BLUE}{root}')
                self._check_and_create_copy(root, self.filename, self.copy_filename)
                self._replace_file(root, self.filename)

    @staticmethod
    def _check_and_create_copy(root_path, orig_filename, copy_filename):
        copy_file_path = os.path.join(root_path, copy_filename)
        orig_file_path = os.path.join(root_path, orig_filename)
        if not os.path.exists(copy_file_path):
            shutil.copy2(orig_file_path, copy_file_path)
            print(f'Создана копия файла: {F_YELLOW}{copy_file_path}')

    def _replace_file(self, root_path, filename):
        orig_file_path = os.path.join(root_path, filename)
        replacement_file_path = os.path.join(self.download_path, filename)
        shutil.copy2(replacement_file_path, orig_file_path)
        print('Старый файл заменен\n')


if __name__ == '__main__':
    finder = FileFinder()
    finder.find_file()
