import os

F_BLUE = '[#2f6ed0]'
F_GREEN = '[#1cc95a]'
F_RED = '[#e94e39]'
F_YELLOW = '[#e5c07b]'
F_GREY = '[#595f6c]'
S_RESET = '[/]'

DEFAULT_META_FILENAME = '.\\meta.json'
DEFAULT_DLSS_FILENAME = 'nvngx_dlss.dll'
DEFAULT_DLSSD_FILENAME = 'nvngx_dlssd.dll'
DEFAULT_DLSSG_FILENAME = 'nvngx_dlssg.dll'
DEFAULT_DOWNLOADS_FOLDER = os.path.expandvars('%USERPROFILE%\\Downloads\\')
DEFAULT_DLSS_URL = 'https://www.techpowerup.com/download/nvidia-dlss-dll/'
DEFAULT_DLSSD_URL = 'https://www.techpowerup.com/download/nvidia-dlss-3-ray-reconstruction-dll/'
DEFAULT_DLSSG_URL = 'https://www.techpowerup.com/download/nvidia-dlss-3-frame-generation-dll/'

CONFIG_TEMPLATE = {
    'title': '',
    'zip_filename': '',
    'dll_filename': '',
    'root_path': '',
    'download_path': '',
    'url': '',
    'options': {}
}
