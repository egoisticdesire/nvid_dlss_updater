from InquirerPy.base import Choice
from rich import print

from scripts.downloader import Downloader
from scripts.extractor import Extractor
from scripts.file_finder import FileFinder
from scripts.metadata import Meta
from scripts.utility import delete_temp_files_by_patterns, prompt_choice_selection
from variables import F_RED


def main():
    meta = Meta()

    try:
        downloader = Downloader(
            meta.config['options'],
            meta.config['download_path'],
        )
        meta.update_config_metadata(
            *downloader.get_data(meta.config['url'])
        )

        extractor = Extractor(
            meta.config['download_path'],
            meta.config['zip_filename'],
            meta.config['dll_filename'],
        )
        extractor.get_data_from_archive()

        finder = FileFinder(
            meta.config['root_path'],
            meta.config['download_path'],
            meta.config['dll_filename'],
        )
        finder.find_and_replace_file()

    except FileNotFoundError:
        print(
            f"Проверьте данные:\n{F_RED}"
            f"\troot_path = {meta.config['root_path']}\n"
            f"\tdownload_path = {meta.config['download_path']}\n"
            f"\turl = {meta.config['url']}\n"
            f"\tdll_filename = {meta.config['dll_filename']}\n"
            f"\tzip_filename = {meta.config['zip_filename']}\n"
        )

    finally:
        patterns = ['*.tmp', '*.crdownload']
        choices_items = {'Да': True, 'Нет': False}
        choices = [Choice(value=value, name=key) for key, value in choices_items.items()]

        def transformer(result: str) -> str:
            if result.lower() == 'да':
                return 'Удаляются загруженные и временные файлы...'
            return 'Удаляются только временные файлы...'

        message = '\nУдалить загруженные файлы? '
        answer = prompt_choice_selection(choices=choices, transformer=transformer, message=message, default=False)

        if answer:
            patterns.extend([meta.config['dll_filename'], meta.config['zip_filename']])

        delete_temp_files_by_patterns(
            meta.config['download_path'],
            *patterns
        )

        input('\nНажмите Enter для выхода...')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyboardInterrupt):
        pass
