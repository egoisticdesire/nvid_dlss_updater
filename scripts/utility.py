import glob
import ujson
import os

from fake_useragent import UserAgent

from variables import (DEFAULT_DLL_FILENAME,
                       DEFAULT_DOWNLOADS_FOLDER,
                       DEFAULT_GAMES_FOLDER,
                       DEFAULT_META,
                       DEFAULT_URL,
                       F_GREEN,
                       F_RED,
                       GAMES_FOLDER_REQUESTED,
                       HEADLESS_MODE_REQUESTED,
                       S_RESET)


class Meta:
    def __init__(self, filename=DEFAULT_META):
        self.filename = filename
        self.data = self.create_metadata()

    def create_metadata(self):
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            with open(self.filename, 'w', encoding='utf-8') as metafile:
                template = {
                    'title': '',
                    'zip_filename': '',
                    'dll_filename': '',
                    'root_path': '',
                    'download_path': '',
                    'url': '',
                    'options': {}
                }
                ujson.dump(template, metafile, indent=4, ensure_ascii=False)

        return self._add_config_to_metadata()

    def update_metadata(self, title, zip_filename):
        self.data['title'] = title
        self.data['zip_filename'] = zip_filename
        return self.data

    def _add_config_to_metadata(self):
        global GAMES_FOLDER_REQUESTED
        global HEADLESS_MODE_REQUESTED

        with open(self.filename, 'r', encoding='utf-8') as metafile:
            config = ujson.load(metafile)
            config['download_path'] = DEFAULT_DOWNLOADS_FOLDER
            config['dll_filename'] = DEFAULT_DLL_FILENAME
            config['url'] = DEFAULT_URL

            if not GAMES_FOLDER_REQUESTED:
                config['root_path'] = get_games_folder()
                GAMES_FOLDER_REQUESTED = True

            if not HEADLESS_MODE_REQUESTED:
                config['options'] = {
                    'accept': '*/*',
                    'user-agent': UserAgent().random,
                    'disable-blink-features': 'AutomationControlled',
                    'headless=new': install_silently()
                }
                HEADLESS_MODE_REQUESTED = True

        with open(self.filename, 'w', encoding='utf-8') as metafile:
            ujson.dump(config, metafile, indent=4, ensure_ascii=False)
        return config


def get_games_folder():
    count = 3
    print(f'Для выхода введите "{F_RED}exit{S_RESET}"')
    while count:
        disk = input('Укажите букву диска, на котором хранятся игры: ')
        if disk.isalpha() and disk.isascii() and len(disk) == 1:
            folder = input('Из какого каталога брать игры (можно оставить поле пустым): ')
            if folder == 'exit'.lower():
                print('Выполнение программы остановлено пользователем')
                exit(0)
            return f'{disk}:\\{folder}\\'.strip()
        elif disk == 'exit'.lower():
            print('Выполнение программы остановлено пользователем')
            exit(0)
        else:
            count -= 1
            print(f'Это не может быть буквой диска! (Попыток осталось: {count})\n')

    print(f'Установлен путь по-умолчанию: {F_GREEN}[{DEFAULT_GAMES_FOLDER}]{S_RESET}\n')
    return DEFAULT_GAMES_FOLDER


def install_silently():
    while True:
        answer = input('По-умолчанию включена "тихая" установка. Продолжить "тихую" установку? (Y/n): ')
        if answer.lower() == 'y' or answer == '':
            return True
        elif answer.lower() == 'n':
            return False
        elif answer == 'exit'.lower():
            print('Выполнение программы остановлено пользователем')
            exit(0)
        else:
            print('Некорректный ввод!\n')


def clearing_temp_files(download_path, *temp_file_pattern):
    for file in temp_file_pattern:
        temp_files = glob.glob(os.path.join(download_path, file))

        for temp_file in temp_files:
            os.remove(temp_file)


if __name__ == '__main__':
    meta = Meta()
    meta.create_metadata()
