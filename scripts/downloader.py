import ujson
import os
import time

import colorama

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from scripts.utility import Meta
from variables import DEFAULT_META, F_BLUE, F_GREEN, S_RESET

colorama.init(autoreset=True)


class Downloader:
    def __init__(self, webdriver_options, download_path):
        self.webdriver_options = webdriver_options
        self.download_path = download_path

    def get_data_from_site(self, url, max_retries=3):
        with self._start_chrome_webdriver() as driver:
            try:
                driver.get(url=url)
                driver.implicitly_wait(10)

                retry_count = 0
                while retry_count < max_retries:
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
                        print('Элемент не найден, страница обновлена')
                        time.sleep(1)
                        driver.refresh()
                        retry_count += 1

            except TimeoutException:
                print('Превышено время ожидания загрузки страницы')

            except Exception as err:
                print(err)

        return latest_version_title, latest_version_filename

    def _start_chrome_webdriver(self):
        chrome_service = ChromeService(ChromeDriverManager().install())
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

    def _check_version(self, version, zip_filename, meta_filename=DEFAULT_META):
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
            self._get_user_choice(ver=data['title'])

    def _check_file_download_status(self, downloaded_file, wait_time=60, file_exists=False):
        download_fullpath = os.path.join(self.download_path, downloaded_file)

        while wait_time > 0:
            if os.path.exists(download_fullpath):
                file_exists = True
                break
            time.sleep(1)
            wait_time -= 1

            if not wait_time:
                wait_time = self._get_user_choice(timeout=True)

        if file_exists:
            print(f'Файл успешно загружен: {F_GREEN}[{download_fullpath}]\n')

    @staticmethod
    def _get_user_choice(timeout: bool = False, ver: str = ''):
        while True:
            if timeout:
                answer = input('Время ожидания превышено\nФайл не загружен, подождать? (Y/n): ')
                if answer.lower() == 'n' or answer == 'exit':
                    print('\nЗагрузка прервана\nВыполнение программы остановлено пользователем')
                    exit(0)
                elif answer.lower() == 'y' or answer == '':
                    print('\nПродолжается загрузка файла...\n')
                    wait_time = 60
                    return wait_time
                else:
                    print('Некорректный ввод\n')

            answer = input(f'Текущая версия {F_BLUE}{ver.upper()}{S_RESET} является актуальной. Продолжить? (y/N): ')
            if answer.lower() == 'n' or answer == 'exit' or answer == '':
                print('\nОбновление не требуется\nВыполнение программы остановлено пользователем')
                exit(0)
            elif answer.lower() == 'y':
                print('\nЗагрузка файла...')
                break
            else:
                print('\nНекорректный ввод!\n')


if __name__ == '__main__':
    meta = Meta()
    config = meta.create_metadata()
    downloader = Downloader(config['options'], config['download_path'])
    downloader.get_data_from_site(config['url'])
