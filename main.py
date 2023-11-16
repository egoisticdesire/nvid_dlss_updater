from rich import print

from scripts.downloader import Downloader
from scripts.extractor import Extractor
from scripts.file_finder import FileFinder
from scripts.utility import delete_temp_files_by_patterns, Meta
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
        finder.find_file()

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
        delete_temp_files_by_patterns(
            meta.config['download_path'],
            '*.tmp',
            '*.crdownload',
        )

        input('\nНажмите Enter для выхода...')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyboardInterrupt):
        pass
