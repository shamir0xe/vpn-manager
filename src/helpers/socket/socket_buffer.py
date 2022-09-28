import socket
from libs.python_library.io.buffer import Buffer


class SocketBuffer(Buffer):
    def __init__(self, sock: socket) -> None:
        self.sock = sock
    
    def read(self, count: int = 1) -> str:
        c = self.sock.recv(count).decode()
        return c
    
    def write(self, string: str) -> None:
        self.sock.sendall(string.encode())
    
    def write_line(self, string: str) -> None:
        self.write(f'{string}\n')
    
    def close(self) -> None:
        self.sock.close()
