from __future__ import annotations

from libs.python_library.io.buffer_reader import BufferReader
from libs.python_library.io.buffer_writer import BufferWriter
from libs.python_library.config.config import Config
from src.actions.node.node_actions import NodeActions
from src.helpers.socket.socket_buffer import SocketBuffer
from src.helpers.log.runtime_log import RuntimeLog
from src.helpers.socket.socket_helper import SocketHelper
from src.mediators.request_mediator import RequestMediator


class ClientMediator:
    def __init__(self, log: RuntimeLog = None) -> None:
        self.log = log
        self.status = True
        self.sock = SocketHelper.TCPIp()
        self.writer = BufferWriter(SocketBuffer(self.sock))
        self.reader = BufferReader(SocketBuffer(self.sock))
    
    def test(self) -> ClientMediator:
        if not self.status:
            return self
        return self
    
    def check_network(self) -> ClientMediator:
        if not self.status:
            return self
        access = NodeActions.access_peer()
        if not access:
            self.status = False
        self.log.add_log(f'peer ping {access}', 'check-network')
        return self
    
    def login(self) -> ClientMediator:
        if not self.status:
            return self
        res = RequestMediator() \
            .append_url('login') \
            .set_payload({
                'username': Config.read('env.server.username'),
                'password': Config.read('env.server.password')
            }) \
            .post() \
            .response()
        if not res.status:
            self.status = False
            self.log.add_log(f'error: {res.response}', 'login')
            return self
        self.log.add_log('successfully logged in', 'login')
        self.token = res.response['token']
        return self
    
    def request_modification(self, port: int, gate_port: int) -> ClientMediator:
        if not self.status:
            return self
        res = RequestMediator() \
            .append_url('change_ports') \
            .set_payload({
                'token': self.token,
                'interface_port': gate_port,
                'peer_port': port
            }) \
            .post() \
            .response()
        if not res.status:
            self.status = False
            self.log.add_log(f'error: {res.response}', 'request-modification')
        self.log.add_log(res.response, 'request-modification')
        return self
