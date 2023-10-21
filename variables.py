import os

from colorama import Fore, Style

F_BLUE = Fore.BLUE
F_GREEN = Fore.GREEN
F_RED = Fore.RED
F_YELLOW = Fore.YELLOW
S_RESET = Style.RESET_ALL

DEFAULT_META = '.\\meta.json'
DEFAULT_DLL_FILENAME = 'nvngx_dlss.dll'
DEFAULT_GAMES_FOLDER = 'D:\\GAMES\\'
DEFAULT_DOWNLOADS_FOLDER = os.path.expandvars('%USERPROFILE%\\Downloads\\')
DEFAULT_URL = 'https://www.techpowerup.com/download/nvidia-dlss-dll/'

GAMES_FOLDER_REQUESTED = False
HEADLESS_MODE_REQUESTED = False
