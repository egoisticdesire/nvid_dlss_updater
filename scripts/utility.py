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
            with open(self.filename, 'w', encoding='utf-8') as file:
                template = {
                    "title": "",
                    "zip_filename": "",
                    "dll_filename": "nvngx_dlss.dll",
                    "root_path": "D:\\GAMES\\",
                    "download_path": os.path.expandvars('%USERPROFILE%\\Downloads\\'),
                    "webdriver_path": ".\\scripts",
                    "url": "https://www.techpowerup.com/download/nvidia-dlss-dll/",
                    "options": {
                        'accept': '*/*',
                        'user-agent': UserAgent().random,
                        'disable-blink-features': 'AutomationControlled',
                        'headless=new': True
                    }
                }
                json.dump(template, file, indent=4, ensure_ascii=False)

        with open(self.filename, 'r', encoding='utf-8') as file:
            return json.load(file)

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
