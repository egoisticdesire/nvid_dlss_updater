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
                    'log-level': 3,
                    'disable-blink-features': 'AutomationControlled',
                    'headless=new': set_silent_mode()
                }
                HEADLESS_MODE_REQUESTED = True

        with open(self.filename, 'w', encoding='utf-8') as metafile:
            ujson.dump(config, metafile, indent=4, ensure_ascii=False)
        return config


def get_games_folder() -> str:
    if os.name != 'nt':
        print('Ваша ОС не относится к семейству Windows')
        sys.exit(0)

    drives = [drive.device for drive in psutil.disk_partitions() if 'cdrom' not in drive.opts]
    message = 'Выберите диск: '
    choices = [Choice(value=drive, name=drive) for drive in drives]
    answer = get_select_prompts_console(choices=choices, message=message, default=drives[0])
    return get_filepath_prompts_console(answer)


def get_select_prompts_console(
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


def get_filepath_prompts_console(drive: str) -> str:
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


def set_silent_mode() -> bool:
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

    answer = get_select_prompts_console(choices=choices, transformer=transformer, message=message)

    if answer is None:
        sys.exit(0)
    return answer


def clearing_temp_files(download_path: str, *temp_file_patterns: str) -> None:
    for file in temp_file_patterns:
        temp_files = glob.glob(os.path.join(download_path, file))

        for temp_file in temp_files:
            os.remove(temp_file)
