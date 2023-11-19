import sys
from pathlib import Path

import psutil
import ujson
from fake_useragent import UserAgent
from InquirerPy.base import Choice

from scripts.utility import prompt_choice_selection, prompt_directory_selection
from variables import (CONFIG_TEMPLATE,
                       DEFAULT_DLSS_FILENAME,
                       DEFAULT_DOWNLOADS_FOLDER,
                       DEFAULT_META_FILENAME,
                       DEFAULT_DLSS_URL)


class Meta:
    def __init__(self, filename: str = DEFAULT_META_FILENAME):
        self.filename = filename
        self.config = self.__set_config_data()

    def update_config_metadata(self, title: str, zip_filename: str) -> dict:
        self.config.update({'title': title, 'zip_filename': zip_filename})
        return self.config

    def __set_config_data(self) -> dict:
        file_path = Path(self.filename)
        file_path.touch(exist_ok=True)

        if file_path.stat().st_size == 0:
            self.__save_config_to_file(is_template=True)

        self.__load_config_from_file()

        self.config.update(
            {
                'download_path': DEFAULT_DOWNLOADS_FOLDER,
                'dll_filename': DEFAULT_DLSS_FILENAME,
                'url': DEFAULT_DLSS_URL,
                'root_path': self.__get_games_folder(),
                'options': {
                    'accept': '*/*',
                    'user-agent': UserAgent().random,
                    'log-level': 3,
                    'disable-blink-features': 'AutomationControlled',
                    'headless=new': self.__set_silent_mode()
                }
            }
        )

        self.__save_config_to_file()

        return self.config

    @staticmethod
    def __get_games_folder() -> str:
        if Path().drive:
            print('Ваша ОС не относится к семейству Windows')
            sys.exit(0)

        drives = [drive.device for drive in psutil.disk_partitions() if 'cdrom' not in drive.opts]
        message = 'Выберите диск: '
        choices = [Choice(value=drive, name=drive) for drive in drives]
        answer = prompt_choice_selection(choices=choices, message=message, default=drives[0])
        return prompt_directory_selection(answer)

    @staticmethod
    def __set_silent_mode() -> bool:
        message = 'Хотите продолжить "тихую" установку? '
        choices_items = {'Да': True, 'Нет': False, 'Выход': None}
        choices = [Choice(value=value, name=key) for key, value in choices_items.items()]

        def transformer(result: str) -> str:
            res = result.lower()
            if res == 'выход':
                return 'Выполнение прервано пользователем'
            elif res == 'да':
                return 'Включена "тихая" установка'
            else:
                return 'Отключена "тихая" установка'

        answer = prompt_choice_selection(choices=choices, transformer=transformer, message=message)

        if answer is None:
            sys.exit(0)
        return answer

    def __save_config_to_file(self, is_template: bool = False) -> None:
        if is_template:
            self.config = CONFIG_TEMPLATE
        with open(self.filename, 'w', encoding='utf-8') as metafile:
            ujson.dump(self.config, metafile, indent=4, ensure_ascii=False, escape_forward_slashes=False)

    def __load_config_from_file(self) -> None:
        with open(self.filename, 'r', encoding='utf-8') as metafile:
            self.config = ujson.load(metafile)
