from __future__ import annotations
import json
import requests
from libs.python_library.config.config import Config
from libs.python_library.data.data_transfer_object import DataTransferObject


class RequestMediator:
    def __init__(self) -> None:
        host, port = Config.read('env.server.ip'), Config.read('env.server.port')
        self.url = f'http://{host}:{port}'
        self.payload = {}
        self.headers = {
            'Content-Type': 'application/json'
        }

    def append_url(self, ex_url: str) -> RequestMediator:
        self.url += '/' + ex_url
        return self
    
    def set_url(self, url: str) -> RequestMediator:
        self.url = url
        return self
    
    def set_payload(self, payload: dict) -> RequestMediator:
        self.payload = payload
        return self
    
    def set_headers(self, headers: dict) -> RequestMediator:
        self.headers = headers
        return self
    
    def post(self, timeout: int = Config.read('main.connection.request_timeout')) -> RequestMediator:
        self.request = requests.post(
            headers=self.headers, 
            url=self.url, 
            json=self.payload,
            timeout=timeout
        )
        return self
    
    def response(self) -> DataTransferObject:
        return DataTransferObject.from_dict(json.loads(self.request.content))
