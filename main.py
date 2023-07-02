import colorama

from scripts.downloader import Downloader
from scripts.extractor import Extractor
from scripts.file_finder import FileFinder
from scripts.utility import clearing_temp_files, Meta
from variables import F_RED

colorama.init(autoreset=True)


def main():
    meta = Meta()
    config = meta.create_metadata()

    try:
        downloader = Downloader(
            config['webdriver_path'],
            config['options'],
            config['download_path'],
        )
        config = meta.update_metadata(
            *downloader.get_data_from_site(config['url'])
        )

        extractor = Extractor(
            config['download_path'],
            config['zip_filename'],
            config['dll_filename'],
        )
        extractor.get_data_from_archive()

        finder = FileFinder(
            config['root_path'],
            config['download_path'],
            config['dll_filename'],
        )
        finder.find_file()

    except FileNotFoundError:
        print(
            f"Пожалуйста проверьте данные:\n{F_RED}"
            f"\troot_path = {config['root_path']}\n"
            f"\tdownload_path = {config['download_path']}\n"
            f"\twebdriver_path = {config['webdriver_path']}\n"
            f"\turl = {config['url']}\n"
            f"\tdll_filename = {config['dll_filename']}\n"
            f"\tzip_filename = {config['zip_filename']}\n"
        )

    finally:
        clearing_temp_files(config['download_path'])


if __name__ == '__main__':
    main()
