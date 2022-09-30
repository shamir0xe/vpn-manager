from __future__ import annotations
from libs.python_library.io.buffer_reader import BufferReader
from libs.python_library.io.buffer_writer import BufferWriter
from libs.python_library.config.config import Config
from src.models.types.server_commands import ServerCommands
from src.actions.node.node_actions import NodeActions
from src.helpers.socket.socket_buffer import SocketBuffer
from src.helpers.log.runtime_log import RuntimeLog
from src.helpers.socket.socket_helper import SocketHelper


class ClientMediator:
    def __init__(self, log: RuntimeLog = None) -> None:
        self.__log = log
        self.status = True
        self.sock = SocketHelper.TCPIp()
        
        self.writer = BufferWriter(SocketBuffer(self.sock))
        self.reader = BufferReader(SocketBuffer(self.sock))
    
    def check_network(self) -> ClientMediator:
        if not self.status:
            return self
        access = NodeActions.access_peer()
        if not access:
            self.status = False
        self.__log.add_log(f'peer ping {access}', 'check-network')
        return self
    
    def login(self) -> ClientMediator:
        if not self.status:
            return self
        try:
            # self.__log.add_log(f'trying to...', 'login')
            ip, port = (Config.read('env.server.ip'), Config.read('env.server.port'))
            self.sock.connect((ip, port))
            self.sock.setblocking(False)
            print('trying to connect')
            username, password = (Config.read('env.server.username'), Config.read('env.server.password'))
            # self.writer.write_line('Hello cruel world')
            # response = self.reader.next_line().strip()
            # print(f'response: {response}')
            # # self.__log.add_log(response, 'login-response')
            # self.status = False
            # return self

            self.writer.write_line(
                f'{username}\n{password}'
            )
            # self.writer.write_line(username)
            # self.writer.write_line(password)
            response = self.reader.next_line().strip()
            # self.__log.add_log(response, 'login-response')
            print(f'reponse: {response}')
            if response != 'OK':
                self.status = False
                print(f'error: {response}')
                # self.__log.add_log(f'error: {response}', 'login')
        except BaseException as err:
            self.status = False
            print(f'exception error: {err}')
            # self.__log.add_log(f'error: {err}', 'login')
        return self
    
    def request_modification(self, port: int, gate_port: int) -> ClientMediator:
        if not self.status:
            return self
        try:
            # self.__log.add_log('sending request', 'request-modification')
            print(f'sending request')
            self.writer.write_line(
                f"{ServerCommands.RUN_MODIFICATION.value} --gate --interface.port {gate_port} --peer.port {port}"
            )
            response = self.reader.next_line().strip()
            # self.__log.add_log(f'response: {response}', 'request-modification')
            print(f'response: {response}')
            if response != 'OK':
                self.status = False
                print(f'error: {response}')
                # self.__log.add_log(f'error: {response}', 'request-modification')
        except BaseException as err:
            self.status = False
            print(f'error: {err}')
            # self.__log.add_log(f'error: {err}', 'request-modification')
        return self

    def request_end(self) -> ClientMediator:
        if not self.status:
            return self
        try:
            # self.__log.add_log('requesting end', 'request-end')
            print(f'requesting end')
            self.writer.write_line(f"{ServerCommands.END.value}")
            response = self.reader.next_line().strip()
            print(f'response: {response}')
            # self.__log.add_log(response, 'request-end')
        except BaseException as err:
            self.status = False
        return self
    
    def close(self) -> ClientMediator:
        try:
            self.sock.close()
        except BaseException as _:
            pass
        return self
