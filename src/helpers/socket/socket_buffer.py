import socket
from libs.python_library.io.buffer import Buffer


class SocketBuffer(Buffer):
    MSG_LEN = 100
    def __init__(self, sock: socket) -> None:
        self.sock = sock
    
    def read(self, count: int = 1) -> str:
        chunks = []
        received_cnt = 0
        while received_cnt < self.MSG_LEN:
            chunk = self.sock.recv(self.MSG_LEN - received_cnt)
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            received_cnt += len(chunk)
        received_str = (b''.join(chunks)).decode()
        # print('~~~ received: ' + received_str)
        return received_str
    
    def write(self, string: str) -> None:
        msg_array = bytearray(string.encode())
        while len(msg_array) < self.MSG_LEN:
            msg_array.extend(bytearray(b' '))
        msg_bytes = bytes(msg_array)
        total_send = 0
        while total_send < self.MSG_LEN:
            sent = self.sock.send(msg_array[total_send:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_send += sent
        # print('~~~ sent successfully')
    
    def write_line(self, string: str) -> None:
        self.write(f'{string}\n')
    
    def close(self) -> None:
        self.sock.close()
