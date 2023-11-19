import shutil
from pathlib import Path

from rich import print

from scripts.metadata import Meta
from variables import F_BLUE, F_GREY, F_YELLOW, S_RESET


class FileFinder:
    def __init__(self, start_directory: str, download_path: str, dll_filename: str):
        self.start_directory = Path(start_directory)
        self.download_path = Path(download_path)
        self.dll_filename = dll_filename
        self.name, self.extension = dll_filename.split('.')
        self.copy_filename = f'{self.name} — копия.{self.extension}'

    def find_and_replace_file(self) -> None:
        self.__process_directory(self.start_directory)

    def __process_directory(self, directory: Path) -> None:
        try:
            for item in directory.iterdir():
                if item.is_dir():
                    self.__process_directory(item)
                elif item.is_file() and item.name == self.dll_filename:
                    print(f'Файл {F_BLUE}{self.dll_filename}{S_RESET} найден в каталоге {F_YELLOW}[{directory}]')
                    self.__create_copy_and_replace(item)
        except PermissionError:
            pass

    def __create_copy_and_replace(self, file_path: Path) -> None:
        copy_file_path = file_path.parent / self.copy_filename
        replacement_file_path = self.download_path / self.dll_filename

        try:
            if not copy_file_path.exists():
                shutil.copy2(file_path, copy_file_path)
                print(f'Создана копия файла: {F_GREY}[{copy_file_path}]')

            shutil.copy2(replacement_file_path, file_path)
            print('Файл заменен\n')

        except (shutil.Error, FileNotFoundError) as err:
            print(f'Произошла ошибка при копировании и замене файла: {err}')


if __name__ == '__main__':
    meta = Meta()
    finder = FileFinder(
        meta.config['root_path'],
        meta.config['download_path'],
        meta.config['dll_filename'],
    )
    finder.find_and_replace_file()
