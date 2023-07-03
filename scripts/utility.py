import glob
import json
import os

from fake_useragent import UserAgent

from variables import DEFAULT_META


class Meta:
    def __init__(self, filename=DEFAULT_META):
        self.filename = filename
        self.data = self.create_metadata()

    def create_metadata(self):
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            with open(self.filename, 'w', encoding='utf-8') as metafile:
                template = {
                    'title': '',
                    'zip_filename': '',
                    'dll_filename': '',
                    'root_path': '',
                    'download_path': '',
                    'webdriver_path': '',
                    'url': '',
                    'options': {}
                }
                json.dump(template, metafile, indent=4, ensure_ascii=False)

        games_folder = 'D:\\GAMES\\'
        return self._add_config_to_metadata(root_path=games_folder, headless=False)

    def _add_config_to_metadata(
        self,
        root_path='C:\\GAMES\\',
        download_path=os.path.expandvars('%USERPROFILE%\\Downloads\\'),
        webdriver_path='.\\scripts',
        headless=True,
    ):
        with open(self.filename, 'r', encoding='utf-8') as metafile:
            config = json.load(metafile)
            config['root_path'] = root_path
            config['download_path'] = download_path
            config['webdriver_path'] = webdriver_path
            # Имя файла, ссылка и опции браузера всегда одинаковые,
            # за исключением запуска браузера в безголовом режиме
            config['dll_filename'] = 'nvngx_dlss.dll'
            config['url'] = 'https://www.techpowerup.com/download/nvidia-dlss-dll/'
            config['options'] = {
                'accept': '*/*',
                'user-agent': UserAgent().random,
                'disable-blink-features': 'AutomationControlled',
                'headless=new': headless
            }

        with open(self.filename, 'w', encoding='utf-8') as metafile:
            json.dump(config, metafile, indent=4, ensure_ascii=False)
        return config

    def update_metadata(self, title, zip_filename):
        self.data['title'] = title
        self.data['zip_filename'] = zip_filename
        return self.data


def clearing_temp_files(download_path):
    temp_file_pattern = ['*.tmp', '*.crdownload']
    for file in temp_file_pattern:
        temp_files = glob.glob(os.path.join(download_path, file))

        for temp_file in temp_files:
            os.remove(temp_file)


if __name__ == '__main__':
    meta = Meta()
    meta.create_metadata()
