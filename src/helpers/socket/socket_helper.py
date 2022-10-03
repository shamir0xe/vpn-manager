import socket


class SocketHelper:
    @staticmethod
    def TCPIp() -> socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock

    @staticmethod
    def TCPIpReusable() -> socket:
        sock = SocketHelper.TCPIp()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock
    
