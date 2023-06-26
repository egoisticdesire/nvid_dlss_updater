import os
from colorama import Fore, Style
from fake_useragent import UserAgent

DEFAULT_ROOT_DIRECTORY = 'D:\\GAMES\\'
DEFAULT_DOWNLOADED_FILES_PATH = os.path.expandvars('%USERPROFILE%\\Downloads\\')
DEFAULT_WEBDRIVER_PATH = '.\\scripts'
DEFAULT_FILENAME = 'nvngx_dlss.dll'
DEFAULT_ZIP_FILENAME = 'nvngx_dlss_3.1.13.zip'

F_BLUE = Fore.BLUE
F_GREEN = Fore.GREEN
F_RED = Fore.RED
F_YELLOW = Fore.YELLOW
S_RESET = Style.RESET_ALL

ARCHIVES = ['zip', 'rar', '7z']

DEFAULT_URL = 'https://www.techpowerup.com/download/nvidia-dlss-dll/'
DEFAULT_OPTIONS = {
    'accept': '*/*',
    'user-agent': UserAgent().random,
    'disable-blink-features': 'AutomationControlled',  # disable webdriver detection
    'headless=new': True  # silent mode True/False
}
