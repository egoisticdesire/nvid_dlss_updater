import os

from colorama import Fore, Style

F_BLUE = '[#2f6ed0]'
F_GREEN = '[#1cc95a]'
F_RED = '[#e94e39]'
F_YELLOW = '[#e5c07b]'
S_RESET = '[/]'

DEFAULT_META = '.\\meta.json'
DEFAULT_DLL_FILENAME = 'nvngx_dlss.dll'
DEFAULT_GAMES_FOLDER = 'D:\\GAMES\\'
DEFAULT_DOWNLOADS_FOLDER = os.path.expandvars('%USERPROFILE%\\Downloads\\')
DEFAULT_URL = 'https://www.techpowerup.com/download/nvidia-dlss-dll/'

GAMES_FOLDER_REQUESTED = False
HEADLESS_MODE_REQUESTED = False
