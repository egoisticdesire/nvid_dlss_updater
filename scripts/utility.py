import glob
import sys
from pathlib import Path
from typing import Callable, List, Optional, Union

import psutil
import ujson
import os

from fake_useragent import UserAgent
from InquirerPy import get_style, inquirer
from InquirerPy.base import Choice
from InquirerPy.validator import PathValidator
from rich import print

from variables import (CONFIG_TEMPLATE,
                       DEFAULT_DLSS_FILENAME,
                       DEFAULT_DOWNLOADS_FOLDER,
                       DEFAULT_META_FILENAME,
                       DEFAULT_URL)


class Meta:
    def __init__(self, filename: str = DEFAULT_META_FILENAME):
        self.filename = filename
        self.config = self.__set_config_data()

    def __save_config_to_file(self, template: bool = False) -> None:
        if template:
            self.config = CONFIG_TEMPLATE
        with open(self.filename, 'w', encoding='utf-8') as metafile:
            ujson.dump(self.config, metafile, indent=4, ensure_ascii=False, escape_forward_slashes=False)

    def __load_config_from_file(self) -> None:
        with open(self.filename, 'r', encoding='utf-8') as metafile:
            self.config = ujson.load(metafile)

    def update_config_metadata(self, title: str, zip_filename: str) -> dict:
        self.config['title'] = title
        self.config['zip_filename'] = zip_filename
        return self.config

    def __set_config_data(self):
        Path(self.filename).touch(exist_ok=True)

        if Path(self.filename).stat().st_size == 0:
            self.__save_config_to_file(template=True)

        self.__load_config_from_file()

        self.config['download_path'] = DEFAULT_DOWNLOADS_FOLDER
        self.config['dll_filename'] = DEFAULT_DLSS_FILENAME
        self.config['url'] = DEFAULT_URL
        self.config['root_path'] = self.__get_games_folder()
        self.config['options'] = {
            'accept': '*/*',
            'user-agent': UserAgent().random,
            'log-level': 3,
            'disable-blink-features': 'AutomationControlled',
            'headless=new': self.__set_silent_mode()
        }

        self.__save_config_to_file()

        return self.config

    @staticmethod
    def __get_games_folder() -> str:
        if os.name != 'nt':
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


def prompt_choice_selection(
    choices: List[Choice], transformer: Optional[Callable] = None,
    message: str = '', default: Union[bool, str] = True
) -> Union[bool, str]:
    style = get_style(
        {
            'pointer': 'fg:#2f6ed0',
            'answer': 'fg:#e5c07b',
            'instruction': 'fg:#595f6c italic',
            'validator': 'fg:#000 bg:#6a4077',
        }, style_override=False
    )

    return inquirer.select(
        message=message,
        qmark='',
        amark='',
        pointer='   ➜ ',
        style=style,
        instruction='<Tab> для переключения ',
        choices=choices,
        transformer=transformer,
        default=default,
    ).execute()


def prompt_directory_selection(drive: str) -> str:
    style = get_style(
        {
            'answer': 'fg:#e5c07b',
            'input': 'fg:#e5c07b',
            'instruction': 'fg:#595f6c italic',
            'validator': 'fg:#000 bg:#6a4077 blink'
        }, style_override=False
    )
    path_validator = PathValidator(is_dir=True, message='Invalid directory path')

    def normalize_directory_path(drive: str, path: str) -> str:
        full_path = Path(drive) / path
        normalized_path = str(full_path.resolve())

        if not normalized_path.endswith('\\'):
            normalized_path += '\\'

        return normalized_path

    return inquirer.filepath(
        message='Выберите директорию: ',
        qmark='',
        amark='',
        style=style,
        instruction='<Tab> для переключения \n     ',
        validate=path_validator,
        only_directories=True,
        filter=lambda path: normalize_directory_path(drive, path),
        transformer=lambda path: normalize_directory_path(drive, path),
        default=drive,
    ).execute()


def delete_temp_files_by_patterns(download_path: str, *temp_file_patterns: str) -> None:
    for file in temp_file_patterns:
        temp_files = glob.glob(os.path.join(download_path, file))

        for temp_file in temp_files:
            os.remove(temp_file)
