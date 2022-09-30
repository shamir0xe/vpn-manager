import errno
import socket
from libs.python_library.io.buffer import Buffer


class SocketBuffer(Buffer):
    MSG_LEN = 100
    def __init__(self, sock: socket) -> None:
        self.sock = sock
    
    def read(self, count: int = 1) -> str:
        while True:
            try:
                print('we are waiting')
                import time
                time.sleep(0.1)
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
    
    def write(self, string: str) -> None:
        msg_array = bytearray(string.encode())
        while len(msg_array) < self.MSG_LEN:
            msg_array.extend(bytearray(b' '))
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
