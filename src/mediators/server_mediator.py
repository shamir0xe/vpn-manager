from __future__ import annotations
from re import I
import socket
from libs.python_library.io.buffer_reader import BufferReader
from libs.python_library.io.buffer_writer import BufferWriter
from src.helpers.bytes.bytes_helper import BytesHelper
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


        self.sock.setblocking(True)
        BUFFER_PADDING = 100
        ENCODING = 'utf-8'
        import time
        for i in range(10):
            print(f'sending {i}')
            self.sock.sendall(BytesHelper.padding(bytes(f'Hello {i}', ENCODING), BUFFER_PADDING))
            time.sleep(.3)

        rec = self.sock.recv(BUFFER_PADDING)
        print(f'received: {rec.decode(ENCODING)}')
        
        print('now sending smt...')
        self.sock.sendall(BytesHelper.padding(b'after receiving, we are sending this', BUFFER_PADDING))

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
        if Authentication.with_username(username, password):
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
    