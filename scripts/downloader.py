import json
import os
import time

import colorama
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from variables import (DEFAULT_DOWNLOAD_PATH, DEFAULT_URL, DEFAULT_WEBDRIVER_PATH,
                       DEFAULT_OPTIONS, F_BLUE, F_GREEN, S_RESET)

colorama.init(autoreset=True)


def get_user_choice(ver: str):
    while True:
        answer = input(f'Текущая версия {F_BLUE}{ver.upper()}{S_RESET} является актуальной. Продолжить? (Y/n): ')
        if answer.lower() == 'n':
            print('\nОбновление не требуется\nВыполнение программы остановлено пользователем')
            exit(0)
        elif answer.lower() == 'y' or answer == '':
            print('\nЗагрузка файла...')
            return


def check_version(version, zip_filename, filename='.\\meta.json'):
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
        get_user_choice(data['title'])


def check_file_download_status(download_path, download_file, wait_time=60, file_exists=False):
    download_fullpath = f'{download_path}{download_file}'

    while wait_time > 0:
        if os.path.exists(download_fullpath):
            file_exists = True
            break
        time.sleep(1)
        wait_time -= 1

    if file_exists:
        print(f'Файл успешно загружен: {F_GREEN}{download_fullpath}\n')


def set_chrome_webdriver_options(options):
    chrome_options = webdriver.ChromeOptions()
    for key, value in options.items():
        if 'headless' in key:
            if value:
                chrome_options.add_argument(key)
        else:
            chrome_options.add_argument(f'{key}={value}')
    return chrome_options


def start_chrome_webdriver(path, options):
    chrome_service = ChromeService(ChromeDriverManager(path=path).install())
    chrome_options = set_chrome_webdriver_options(options)
    return webdriver.Chrome(service=chrome_service, options=chrome_options)


def get_data_from_site(url, max_retries=3):
    with start_chrome_webdriver(path=DEFAULT_WEBDRIVER_PATH, options=DEFAULT_OPTIONS) as driver:
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

                    check_version(latest_version_title, latest_version_filename)

                    latest_version.find_element(
                        by=By.CLASS_NAME,
                        value='download-version-form',
                    ).click()

                    driver.find_element(
                        by=By.CLASS_NAME,
                        value='closest',
                    ).click()

                    check_file_download_status(DEFAULT_DOWNLOAD_PATH, latest_version_filename)

                    break
                except NoSuchElementException:
                    print('Element not found')
                    driver.refresh()
                    retry_count += 1

        except Exception as err:
            print(err)


def main():
    get_data_from_site(DEFAULT_URL)


if __name__ == '__main__':
    main()
