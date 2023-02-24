import json
from core.pools import Pool
from core.suggestions import SuggestionTable

class UserSettings:
    # Default settings values
    pools = []
    text_formats = {'txt', 'md', 'html', 'py',
                    'cpp', 'json'}
    file_preview_text_line_limit = 100
    
    _st : SuggestionTable
    _file_path : str 

    def __init__(self, filepath):
        self._st = SuggestionTable()
        self._file_path = filepath
        self.read()
    
    @property
    def suggestion_table(self):
        return self._st

    def read(self):
        with open(self._file_path) as file:
            self.parse_json(file)
    
    def write(self):
        with open(self._file_path, mode="w") as file:
            self.dump_json(file)

    def parse_json(self, file):
        dic = json.load(file)
        if "pools" in dic:
            self.pools = []
            for poold in dic["pools"]:
                pool = Pool.from_json(poold)
                self.pools.append(pool)
                self._st.add_pool(pool)
        if "text_formats" in dic:
            self.text_formats = dic["text_formats"]
        if "file_preview_text_line_limit" in dic:
            self.file_preview_text_line_limit = dic["file_preview_text_line_limit"]
    
    def dump_json(self, file):
        dic = {}

        pools = []
        for pool in self.pools:
            pools.append(pool.to_json())
        
        dic["pools"] = pools
        dic["text_formats"] = self.text_formats
        dic["file_preview_text_line_limit"] = self.file_preview_text_line_limit

        json.dump(dic, file)
