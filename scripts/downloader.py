import os
import sys
import time

import colorama
import ujson
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from scripts.utility import Meta
from variables import DEFAULT_META, F_BLUE, F_YELLOW, S_RESET

colorama.init(autoreset=True)


class Downloader:
    def __init__(self, webdriver_options: dict, download_path: str):
        self.webdriver_options = webdriver_options
        self.download_path = download_path

    def get_data(self, url: str, max_retries: int = 3) -> tuple:
        with self.__start_chrome_webdriver() as driver:
            try:
                driver.get(url=url)
                driver.implicitly_wait(10)

                for _ in range(max_retries):
                    try:
                        versions_list = driver.find_elements(
                            by=By.CLASS_NAME,
                            value='version',
                        )

                        latest_version = versions_list[0]

                        latest_version_title = latest_version.find_element(
                            by=By.CLASS_NAME,
                            value='title',
                        ).text.strip()

                        latest_version_filename = latest_version.find_element(
                            by=By.CLASS_NAME,
                            value='filename',
                        ).text.strip()

                        self.__check_version(latest_version_title, latest_version_filename)

                        latest_version.find_element(
                            by=By.CLASS_NAME,
                            value='download-version-form',
                        ).click()

                        driver.find_element(
                            by=By.CLASS_NAME,
                            value='closest',
                        ).click()

                        self.__check_file_download_status(latest_version_filename)

                        return latest_version_title, latest_version_filename

                    except NoSuchElementException:
                        time.sleep(1)
                        driver.refresh()

                return None, None

            finally:
                driver.quit()

    def __start_chrome_webdriver(self) -> webdriver.Chrome:
        options = self.__set_chrome_webdriver_options()
        return webdriver.Chrome(options=options)

    def __set_chrome_webdriver_options(self) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        webdriver_options = self.webdriver_options.items()

        for key, value in webdriver_options:
            if 'headless' in key:
                options.add_argument(key) if value else None
            else:
                options.add_argument(f'{key}={value}')

        return options

    def __check_version(self, version: str, zip_filename: str, meta_filename: str = DEFAULT_META) -> None:
        version = version.lower()
        zip_filename = zip_filename.lower()
        with open(meta_filename, 'r', encoding='utf-8') as file:
            data = ujson.load(file)

        if data['title'] != version or data['zip_filename'] != zip_filename:
            print('\nЗагрузка файла...')
            data['title'] = version
            data['zip_filename'] = zip_filename
            with open(meta_filename, 'w', encoding='utf-8') as file:
                ujson.dump(data, file, indent=4, ensure_ascii=False)
        else:
            self.__get_user_choice(ver=data['title'])

    def __check_file_download_status(self, downloaded_file: str, wait_time: int = 60, file_exists: bool = False):
        download_fullpath = os.path.join(self.download_path, downloaded_file)

        while wait_time > 0:
            if os.path.exists(download_fullpath):
                file_exists = True
                break
            time.sleep(1)
            wait_time -= 1

            if not wait_time:
                wait_time = self.__get_user_choice(timeout=True)

        if file_exists:
            print(f'Файл успешно загружен: {F_YELLOW}[{download_fullpath}]\n')

    @staticmethod
    def __get_user_choice(timeout: bool = False, ver: str = '') -> int:
        while True:
            if timeout:
                answer = input('Время ожидания превышено\nФайл не загружен, подождать? (Y/n): ')
                if answer.lower() == 'n' or answer.lower() == 'exit':
                    print('\nЗагрузка прервана\nВыполнение программы остановлено пользователем')
                    sys.exit(0)
                elif answer.lower() == 'y' or answer == '':
                    print('\nПродолжается загрузка файла...\n')
                    wait_time = 60
                    return wait_time
                else:
                    print('Некорректный ввод\n')

            answer = input(f'Текущая версия {F_BLUE}{ver.upper()}{S_RESET} является актуальной. Продолжить? (y/N): ')
            if answer.lower() == 'n' or answer.lower() == 'exit' or answer == '':
                print('\nОбновление не требуется\nВыполнение программы остановлено пользователем')
                sys.exit(0)
            elif answer.lower() == 'y':
                print('\nЗагрузка файла...')
                break
            else:
                print('\nНекорректный ввод!\n')


if __name__ == '__main__':
    meta = Meta()
    config = meta.create_metadata()
    downloader = Downloader(config['options'], config['download_path'])
    downloader.get_data(config['url'])
