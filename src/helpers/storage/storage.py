from __future__ import annotations
from typing import Any, Tuple
from libs.python_library.file.file import File
from libs.python_library.path.path import Path
from libs.python_library.json.json_helper import JsonHelper
import json


class Storage:
    def __init__(self, filename: str) -> None:
        filename += '.json'
        self.path = Path.from_root('storage', filename)
        self.json = File.read_json(self.path)
    
    def get_value(self, selector: str = '', default: Any = None) -> Any:
        print(f'{selector}')
        value = JsonHelper.selector_get_value(self.json, selector)
        if value == {}:
            return default
        return value
    
    def set_value(self, selector: str = '', value: Any = None) -> Storage:
        self.json = JsonHelper.selector_set_value(self.json, selector, value)
        return self
    
    def write(self) -> Storage:
        File.write_file(self.path, json.dumps(self.json))
        return self
    
    @staticmethod
    def extract(selector: str) -> Tuple[str, str]:
        index = selector.find('.')
        if index < 0:
            return (selector, '')
        filename = selector[:index]
        selector = selector[index + 1:]
        return (filename, selector)

    @staticmethod
    def save(selector: str, value: Any) -> None:
        filename, selector = Storage.extract(selector)
        Storage(filename) \
            .set_value(selector, value) \
            .write()
        
    @staticmethod
    def load(selector: str) -> Any:
        filename, selector = Storage.extract(selector)
        return Storage(filename).get_value(selector)
