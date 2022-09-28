from libs.python_library.config.config import Config


class Authentication:
    @staticmethod
    def withUsername(username: str, password: str) -> bool:
        return username == Config.read('env.server.username') and \
            password == Config.read('env.server.password')
