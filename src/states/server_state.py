from libs.python_library.config.config import Config
from bottle import run
from src.apps.middleman_app import middleman_app


class ServerState:
    @staticmethod
    def run():
        host, port = (Config.read('env.server.ip'), Config.read('env.server.port'))
        run(middleman_app, host=host, port=port, debug=True)
