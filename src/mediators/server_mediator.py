from __future__ import annotations
import socket
from src.helpers.log.runtime_log import RuntimeLog
from libs.python_library.io.buffer_reader import BufferReader
from libs.python_library.io.buffer_writer import BufferWriter
from src.helpers.socket.socket_buffer import SocketBuffer
from src.actions.server.authentication import Authentication
from src.resolvers.request_resolver import RequestResolver


class ServerMediator:
    def __init__(self, sock: socket, log: RuntimeLog) -> None:
        self.status = True
        self.sock = sock
        self.log = log
        self.reader = BufferReader(SocketBuffer(sock))
        self.writer = BufferWriter(SocketBuffer(sock))
    
    def auth(self) -> ServerMediator:
        if not self.status:
            return self
        self.log.add_log('Authentication: ')
        username = self.reader.next_line()[:-1]
        password = self.reader.next_line()[:-1]
        self.log.add_log(f'({username}, {password})', 'login-attempt')
        if Authentication.withUsername(username, password):
            self.writer.write_line('OK')
            self.log.add_log('user logged in', 'login')
        else:
            self.log.add_log('invalid credentials', 'login')
            self.writer.write_line('invalid credentials')
            self.status = False
        return self
    
    def resolve_loop(self) -> ServerMediator:
        if not self.status:
            return self
        loop = True
        while loop:
            self.log.add_log('in the loop', 'resolve-loop')
            loop &= RequestResolver(
                reader=self.reader,
                writer=self.writer,
                log=self.log,
            ).do()
        return self
    