from __future__ import annotations
from libs.python_library.config.config import Config
from libs.python_library.file.file import File
from src.helpers.log.runtime_log import RuntimeLog
from libs.python_library.path.path import Path
from libs.python_library.json.json_helper import JsonHelper
from src.models.types.node_types import NodeTypes


class ExtensionBuilder:
    def __init__(
        self,
        node_type: NodeTypes,
        config: dict,
        log: RuntimeLog = None
    ) -> None:
        self.node_type = node_type
        self.config = config
        self.log = log
        self.template = ''
    
    def append_core(self) -> ExtensionBuilder:
        self.template = File.read_file(
            Path.from_root(*Config.read(f'main.{self.node_type.value}.template_path'))
        )
        contents = [JsonHelper.selector_get_value(
            self.config, selector
        ) for selector in Config.read(f'{self.node_type.value}.order')]
        self.template = self.template.format(*contents)
        self.template += '\n'
        return self

    def append_before(self) -> ExtensionBuilder:
        extension_list = Config.read(f'main.{self.node_type.value}.extensions.before')
        if extension_list is None:
            return self
        res = ''
        for path in extension_list:
            res += File.read_file(
                Path.from_root(*path)
            )
            res += '\n'
        self.template = res + self.template
        return self

    def append_after(self) -> ExtensionBuilder:
        extension_list = Config.read(f'main.{self.node_type.value}.extensions.after')
        if extension_list is None:
            return self
        res = ''
        for path in extension_list:
            res += File.read_file(
                Path.from_root(*path)
            )
            res += '\n'
        self.template = self.template + res
        return self
    
    def get_template(self) -> str:
        return self.template
