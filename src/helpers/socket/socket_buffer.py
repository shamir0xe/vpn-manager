import errno
import socket
from libs.python_library.io.buffer import Buffer


class SocketBuffer(Buffer):
    HEADER_LEN = 10
    CODEC = 'utf-8'
    def __init__(self, sock: socket) -> None:
        self.sock = sock
    
    def read_exact_count(self, count: int) -> str:
        while True:
            try:
                chunks = []
                received_cnt = 0
                while received_cnt < count:
                    chunk = self.sock.recv(count - received_cnt)
                    if len(chunk) <= 0:
                        raise RuntimeError("socket connection broken")
                    chunks.append(chunk)
                    received_cnt += len(chunk)
                received_str = (b''.join(chunks)).decode(self.CODEC)
                # print('~~~ received: ' + received_str)
                return received_str
            except IOError as e:
                # This is normal on non blocking connections - when there are no incoming data error is going to be raised
                # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
                # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
                # If we got different error code - something happened
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    raise e

                # We just did not receive anything
                continue

    def read(self, _) -> str:
        msg_len = int(self.read_exact_count(self.HEADER_LEN).strip())
        return self.read_exact_count(msg_len)
    
    def write(self, string: str) -> None:
        msg_bytes = string.encode(self.CODEC)
        header = f'{len(msg_bytes):<{self.HEADER_LEN}}'.encode(self.CODEC)
        msg_bytes = header + msg_bytes
        total_send = 0
        while total_send < len(msg_bytes):
            sent = self.sock.send(msg_bytes[total_send:])
            if sent <= 0:
                raise RuntimeError("socket connection broken")
            total_send += sent
        # print('~~~ sent successfully')
    
    def write_line(self, string: str) -> None:
        self.write(f'{string}\n')
    
    def close(self) -> None:
        self.sock.close()
