from multiprocessing import Process
from libs.python_library.config.config import Config
from src.helpers.log.runtime_log import RuntimeLog
from src.helpers.socket.socket_helper import SocketHelper
from src.mediators.server_mediator import ServerMediator


class ServerState:
    @staticmethod
    def run():
        import socket
        from libs.python_library.io.buffer_reader import BufferReader
        from libs.python_library.io.buffer_writer import BufferWriter
        from src.helpers.socket.socket_buffer import SocketBuffer

        HOST = '127.0.0.1'   # Symbolic name meaning all available interfaces
        # HOST = '185.235.40.240'   # Symbolic name meaning all available interfaces
        PORT = 50007              # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            writer, reader = BufferWriter(SocketBuffer(conn)), BufferReader(SocketBuffer(conn))
            with conn:
                print('Connected by', addr)
                try:
                    while True:
                        data = reader.next_line().strip()
                        print('recieved : ' + data)
                        writer.write_line('OK')
                except BaseException as err:
                    print(f'err: {err}')

        log = RuntimeLog(*Config.read('main.server.log.path'))
        log.add_log('server started', 'server-state')
        log.add_log(f'listening to {Config.read("env.server.ip")}:{Config.read("env.server.port")}', 'server-state')
        sock = SocketHelper.TCPIp()
        sock.bind((Config.read('env.server.ip'), Config.read('env.server.port')))
        sock.listen(1)
        try:
            log.add_log('waiting for a client', 'client-wait')
            while True:
                conn_socket, address = sock.accept()
                conn_socket.setblocking(False)
                def main():
                    log.add_log(f'client {address} connected', 'client-req')
                    try:
                        ServerMediator(sock=conn_socket, log=log) \
                            .auth() \
                            .resolve_loop()
                    except BaseException as err:
                        log.add_log(f'error: {err}', 'runtime-error')
                    return 0
                process = Process(target=main)
                process.start()
                process.join(Config.read('main.connection.total_timeout'))
                process.terminate()
                if process.exitcode is None:
                    log.add_log('error: timeout', 'main-server')
                conn_socket.close()
                log.add_log('\nwaiting for a client', 'client-wait')
        except BaseException as err:
            log.add_log(f'error: {err}', 'main-server')
        finally:
            sock.shutdown(1)
            sock.close()
