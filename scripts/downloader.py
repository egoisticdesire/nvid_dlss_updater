import sys
import time
from pathlib import Path

import ujson
from InquirerPy.base import Choice
from rich import print
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from scripts.metadata import prompt_choice_selection
from variables import DEFAULT_META_FILENAME, F_GREEN, F_YELLOW, S_RESET


class Downloader:
    def __init__(self, webdriver_options: dict, download_path: str, meta_filename: str = DEFAULT_META_FILENAME, timeout: int = 60):
        self.webdriver_options = webdriver_options
        self.download_path = download_path
        self.meta_filename = meta_filename
        self.timeout = timeout

    def get_data(self, url: str, max_retries: int = 3) -> tuple:
        with self.__start_chrome_webdriver() as driver:
            try:
                driver.get(url=url)
                driver.maximize_window()
                driver.implicitly_wait(10)

                for _ in range(max_retries):
                    try:
                        versions_list = driver.find_elements(by=By.CLASS_NAME, value='version')
                        latest_version = versions_list[0]
                        latest_version_title = latest_version.find_element(by=By.CLASS_NAME, value='title').text.strip()
                        latest_version_filename = latest_version.find_element(by=By.CLASS_NAME, value='filename').text.strip()
                        self.__check_version(latest_version_title, latest_version_filename)
                        latest_version.find_element(by=By.CLASS_NAME, value='download-version-form').click()
                        driver.find_element(by=By.CLASS_NAME, value='closest').click()
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
        options.set_capability('browserVersion', '118')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        webdriver_options = self.webdriver_options.items()

        for key, value in webdriver_options:
            if 'headless' in key:
                options.add_argument(key) if value else None
            else:
                options.add_argument(f'{key}={value}')

        return options

    def __check_version(self, version: str, zip_filename: str) -> None:
        version = version.lower()
        zip_filename = zip_filename.lower()

        with open(self.meta_filename, 'r', encoding='utf-8') as file:
            data = ujson.load(file)

        if data['title'] != version or data['zip_filename'] != zip_filename:
            data['title'] = version
            data['zip_filename'] = zip_filename

            with open(self.meta_filename, 'w', encoding='utf-8') as file:
                ujson.dump(data, file, indent=4, ensure_ascii=False, escape_forward_slashes=False)
        else:
            self.__get_user_choice(version=data['title'])

    def __check_file_download_status(self, downloaded_file: str) -> None:
        download_fullpath = Path(self.download_path) / downloaded_file
        time_left = self.timeout

        while time_left > 0:
            if download_fullpath.exists():
                print(f'\nФайл успешно загружен: {F_YELLOW}[{download_fullpath}]\n')
                return

            time.sleep(1)
            time_left -= 1

            if not time_left:
                self.__get_user_choice(timeout=True)

    def __get_user_choice(self, timeout: bool = False, version: str = '') -> int:
        choices_items = {'Да': True, 'Нет': False}
        choices = [Choice(value=value, name=key) for key, value in choices_items.items()]

        def transformer(result: str) -> str:
            if result.lower() == 'да':
                return 'Пожалуйста, подождите...'
            return 'Выполнение прервано пользователем'

        while True:
            if timeout:
                message = 'Файл загружается долго. Желаете подождать? '
                answer = prompt_choice_selection(choices=choices, transformer=transformer, message=message)
                if answer:
                    return self.timeout
                else:
                    sys.exit(0)

            if version:
                print(f'\nТекущая версия {F_GREEN}{version.upper()}{S_RESET} является актуальной.')
                message = 'Всё равно продолжить? '
                answer = prompt_choice_selection(choices=choices, transformer=transformer, message=message, default=False)
                if answer:
                    break
                else:
                    sys.exit(0)
