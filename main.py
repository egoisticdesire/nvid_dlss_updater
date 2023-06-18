import os
import shutil
from colorama import init, Fore, Style

init(autoreset=True)


def find_and_copy_file(root_directory, downloaded_files_directory, orig_file):
    file, extension = orig_file.split('.')
    copy_suffix = ' — копия'

    for root, dirs, files in os.walk(root_directory):
        if f'{file}.{extension}' in files:
            print(f'Файл {Fore.BLUE}{file}.{extension}{Style.RESET_ALL} '
                  f'найден в каталоге {Fore.BLUE}{root}{Style.RESET_ALL}')

            original_file_path = os.path.join(root, f'{file}.{extension}')

            if not os.path.exists(f'{root}\\{file} — копия.{extension}'):
                # Создаем копию файла с суффиксом '— копия'
                copy_file_path = os.path.join(root, f'{file}{copy_suffix}.{extension}')
                shutil.copy2(original_file_path, copy_file_path)
                print(f'Создана копия файла: {Fore.YELLOW}{copy_file_path}{Style.RESET_ALL}')

            # Заменяем оригинал файлом из другого каталога
            replacement_file_path = os.path.join(downloaded_files_directory, f'{file}.{extension}')
            shutil.copy2(replacement_file_path, original_file_path)

            print(f'Оригинал файла заменен на файл из каталога: {Fore.GREEN}{downloaded_files_directory}{Style.RESET_ALL}\n')
            print()


# directory_games = input('Путь к папке с играми:\n> ')
directory_games = 'D:\\GAMES'
downloaded_files_path = os.path.expandvars('%USERPROFILE%\\Downloads')
filename = "nvngx_dlss.dll"

if __name__ == '__main__':
    find_and_copy_file(directory_games, downloaded_files_path, filename)
