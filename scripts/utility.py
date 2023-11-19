from pathlib import Path
from typing import Callable, List, Optional, Union

from InquirerPy import get_style, inquirer
from InquirerPy.base import Choice
from InquirerPy.validator import PathValidator


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
    for pattern in temp_file_patterns:
        temp_files = Path(download_path).glob(pattern)

        for temp_file in temp_files:
            temp_file.unlink(missing_ok=True)
