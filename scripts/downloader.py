import json
import os
import time

import colorama

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from variables import (DEFAULT_DOWNLOAD_PATH, DEFAULT_URL, DEFAULT_WEBDRIVER_PATH,
                       DEFAULT_WEBDRIVER_OPTIONS, F_BLUE, F_GREEN, S_RESET)

colorama.init(autoreset=True)


class Downloader:
    def __init__(
        self,
        webdriver_path=DEFAULT_WEBDRIVER_PATH,
        webdriver_options=DEFAULT_WEBDRIVER_OPTIONS,
        download_path=DEFAULT_DOWNLOAD_PATH
    ):
        self.webdriver_path = webdriver_path
        self.webdriver_options = webdriver_options
        self.download_path = download_path

    def get_data_from_site(self, url=DEFAULT_URL, max_retries=3):
        with self._start_chrome_webdriver() as driver:
            try:
                driver.get(url=url)
                driver.implicitly_wait(10)

                retry_count = 0
                while retry_count < max_retries:
                    try:
                        latest_version = driver.find_elements(
                            by=By.CLASS_NAME,
                            value='version',
                        )[0]

                        latest_version_title = latest_version.find_element(
                            by=By.CLASS_NAME,
                            value='title',
                        ).text.strip()

                        latest_version_filename = latest_version.find_element(
                            by=By.CLASS_NAME,
                            value='filename',
                        ).text.strip()

                        self._check_version(latest_version_title, latest_version_filename)

                        latest_version.find_element(
                            by=By.CLASS_NAME,
                            value='download-version-form',
                        ).click()

                        driver.find_element(
                            by=By.CLASS_NAME,
                            value='closest',
                        ).click()

                        self._check_file_download_status(latest_version_filename)

                        break
                    except NoSuchElementException:
                        print('Элемент не найден')
                        driver.refresh()
                        retry_count += 1

            except TimeoutException:
                print('Превышено время ожидания загрузки страницы')

            except Exception as err:
                print(err)

    def _start_chrome_webdriver(self):
        chrome_service = ChromeService(ChromeDriverManager(path=self.webdriver_path).install())
        chrome_options = self._set_chrome_webdriver_options()
        return webdriver.Chrome(service=chrome_service, options=chrome_options)

    def _set_chrome_webdriver_options(self):
        chrome_options = webdriver.ChromeOptions()
        for key, value in self.webdriver_options.items():
            if 'headless' in key:
                if value:
                    chrome_options.add_argument(key)
            else:
                chrome_options.add_argument(f'{key}={value}')
        return chrome_options

    def _check_version(self, version, zip_filename, filename='.\\meta.json'):
        version = version.lower()
        zip_filename = zip_filename.lower()
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if data.get('title') != version or data.get('zip_filename') != zip_filename:
            print('\nЗагрузка файла...')
            data['title'] = version
            data['zip_filename'] = zip_filename
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        else:
            self._get_user_choice(data['title'])

    def _check_file_download_status(self, download_file, wait_time=60, file_exists=False):
        download_fullpath = os.path.join(self.download_path, download_file)

        while wait_time > 0:
            if os.path.exists(download_fullpath):
                file_exists = True
                break
            time.sleep(1)
            wait_time -= 1

        if file_exists:
            print(f'Файл успешно загружен: {F_GREEN}{download_fullpath}\n')

    @staticmethod
    def _get_user_choice(ver: str):
        while True:
            answer = input(f'Текущая версия {F_BLUE}{ver.upper()}{S_RESET} является актуальной. Продолжить? (Y/n): ')
            if answer.lower() == 'n':
                print('\nОбновление не требуется\nВыполнение программы остановлено пользователем')
                exit(0)
            elif answer.lower() == 'y' or answer == '':
                print('\nЗагрузка файла...')
                return


if __name__ == '__main__':
    downloader = Downloader()
    downloader.get_data_from_site()
