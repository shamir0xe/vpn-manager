from abc import ABC
from typing import Any, Tuple, Union
import bottle
from src.actions.server.response_generator import ResponseGenerator


class Resolver(ABC):
    def __init__(
        self, 
        request: bottle.request, 
        response: bottle.response
    ) -> None:
        self.request = request
        self.response = response
    
    def do(self, *args, **kwargs) -> Any: 
        try:
            self.request.content_type = 'application/json'
            self.response.content_type = 'application/json'
            status, result = self.resolve(*args, **kwargs)
            return ResponseGenerator.generate(status, result)
        except BaseException as err:
            return ResponseGenerator.generate(False, str(err))

    def resolve(self, *args, **kwargs) -> Tuple[bool, Union[dict, str]]:
        return (True, {})

