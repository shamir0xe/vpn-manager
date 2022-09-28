from __future__ import annotations
from datetime import datetime
from libs.python_library.path.path import Path
from libs.python_library.io.buffer_writer import BufferWriter
from libs.python_library.io.file_buffer import FileBuffer


class RuntimeLog:
    def __init__(self, *path) -> None:
        self.log = BufferWriter(FileBuffer(
            Path.from_root(*path),
            "a+"
        ))

    def add(self, log: str) -> RuntimeLog:
        log = log.replace('\n', ' ').replace('\t', ' ')
        self.log.write_line(
            f'[{self.timestamp()}]: {log}'
        ).flush()
        print(log)
        return self
    
    def add_log(self, log: str, name: str = "main-stream") -> RuntimeLog:
        self.add(f'[ {name} ] {log}')
        return self
    
    def close(self) -> RuntimeLog:
        self.log.close()
        return self

    @staticmethod
    def timestamp() -> str:
        return datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
