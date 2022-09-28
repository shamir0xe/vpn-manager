import socket


class SocketHelper:
    @staticmethod
    def TCPIp() -> socket:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

