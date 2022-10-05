from src.helpers.server.token_generator import TokenGenerator
from libs.python_library.config.config import Config
from src.helpers.storage.storage import Storage


class Authentication:
    @staticmethod
    def with_username(username: str, password: str) -> bool:
        return username == Config.read('env.server.username') and \
            password == Config.read('env.server.password')
    
    @staticmethod
    def create_token() -> str:
        token = TokenGenerator.generate(20)
        Storage.save('main.token', token)
        return token
    
    @staticmethod
    def check_token(token: str) -> bool:
        real_token = Storage.load('main.token')
        return token == real_token
