import json
from pathlib import Path

from adapters.imdb_adapter import FileReader


class FileReaderAdapter(FileReader):
    file_name = 'data.json'

    def __init__(self):
        self.path = Path(__file__).parent / f'./{self.file_name}'

    def get_json_obj_from_file(self):
        with self.path.open() as file:
            json_str = file.read()
            obj = json.loads(json_str)
        return obj

    def write_json_to_file(self, json_obj):
        with self.path.open('r+') as file:
            file.write(json_obj)
