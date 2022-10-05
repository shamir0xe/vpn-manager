from typing import Union


class ResponseGenerator:
    @staticmethod
    def generate(status: bool, res: Union[dict, str]):
        return {
            'status': status,
            'response': res
        } 
