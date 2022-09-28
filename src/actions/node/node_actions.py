import random
from libs.python_library.argument.argument_parser import ArgumentParser
from libs.python_library.config.config import Config
from src.models.types.node_types import NodeTypes
from src.helpers.terminal.single_process import SingleProcess


class NodeActions:
    @staticmethod
    def extract_type() -> NodeTypes:
        res = NodeTypes.MIDDLEMAN
        if ArgumentParser.is_option(Config.read('main.gate.name')):
            res = NodeTypes.GATE
        return res
    
    @staticmethod
    def extract_peer_type() -> NodeTypes:
        res = NodeTypes.MIDDLEMAN
        if NodeActions.extract_type() is NodeTypes.MIDDLEMAN:
            res = NodeTypes.GATE
        return res

    @staticmethod
    def access_peer() -> bool:
        peer_type = NodeActions.extract_peer_type()
        ip = Config.read(f'env.{peer_type.value}.ip')
        _, err = SingleProcess(
            'ping', '-c', '1', '-W', Config.read('main.connection.timeout'), ip
        ).run().communicate()
        if err != '':
            return False
        return True

    @staticmethod
    def access_youtube() -> bool:
        hostname = "youtube.com"
        out, err = SingleProcess(
            'ping', '-c', '1', '-W', Config.read('main.connection.timeout'), hostname
        ).run().communicate()
        if err != '' or '0 received' in out:
            return False
        return True

    @staticmethod
    def random_port() -> int:
        port = -1
        ports_list = [
            Config.read('main.gate.interface.port'), 
            Config.read('main.middleman.interface.port'),
            Config.read('env.server.port')
        ]
        while port == -1 or port in ports_list:
            port = random.randint(49152, 65535) # private ports
            if not port in ports_list:
                break
        return port
