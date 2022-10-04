from __future__ import annotations
from re import I
import socket
from libs.python_library.io.buffer_reader import BufferReader
from libs.python_library.io.buffer_writer import BufferWriter
from src.helpers.log.runtime_log import RuntimeLog
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
    
    def test(self) -> ServerMediator:
        if not self.status:
            return self

        import time
        print('sending 1')
        self.writer.write('we are the server, welcome! ')
        time.sleep(1)
        print('sending 2')
        self.writer.write('we can say a lot! ')
        time.sleep(1)
        print('sending 3')
        self.writer.write('just believe in us! ')
        time.sleep(1)

        rec = self.reader.next_string()
        rec += ' ' + self.reader.next_string()
        rec += ' ' + self.reader.next_string()
        rec += ' ' + self.reader.next_string()
        rec += ' ' + self.reader.next_string()
        rec += ' ' + self.reader.next_string()
        rec += ' ' + self.reader.next_string()
        print(f'received: {rec}')
        
        self.writer.write('it is a test, obv! ')
        self.writer.write('last one, I swear! ')

        print('delay for 3 secs')
        import time
        time.sleep(3)

        # print('waiting to close socket')
        # time.sleep(6)

        return self
    
    def auth(self) -> ServerMediator:
        if not self.status:
            return self
        self.log.add_log('Authentication: ')
        username = self.reader.next_line().strip()
        password = self.reader.next_line().strip()
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
    