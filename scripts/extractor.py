import zipfile
from pathlib import Path

from scripts.metadata import Meta


class Extractor:
    def __init__(self, zip_path, zip_filename):
        self.zip_path = zip_path
        self.zip_fullpath = Path(self.zip_path) / zip_filename

    def get_data_from_archive(self) -> None:
        with zipfile.ZipFile(str(self.zip_fullpath), 'r', metadata_encoding='utf-8') as zip_file:
            zip_file.extractall(self.zip_path)


if __name__ == '__main__':
    meta = Meta()
    extractor = Extractor(
        meta.config['download_path'],
        meta.config['zip_filename'],
    )
    extractor.get_data_from_archive()
