import os
from colorama import Fore, Style
from fake_useragent import UserAgent

DEFAULT_FILENAME = 'nvngx_dlss.dll'
DEFAULT_ZIP_FILENAME = 'nvngx_dlss_3.1.13.zip'
DEFAULT_URL = 'https://www.techpowerup.com/download/nvidia-dlss-dll/'

DEFAULT_ROOT_PATH = 'D:\\GAMES\\'
DEFAULT_DOWNLOAD_PATH = os.path.expandvars('%USERPROFILE%\\Downloads\\')
DEFAULT_WEBDRIVER_PATH = '.\\scripts'

DEFAULT_WEBDRIVER_OPTIONS = {
    'accept': '*/*',
    'user-agent': UserAgent().random,
    'disable-blink-features': 'AutomationControlled',  # disable webdriver detection
    'headless=new': False  # silent mode True/False
}

F_BLUE = Fore.BLUE
F_GREEN = Fore.GREEN
F_RED = Fore.RED
F_YELLOW = Fore.YELLOW
S_RESET = Style.RESET_ALL
