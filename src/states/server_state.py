from multiprocessing import Process
from libs.python_library.config.config import Config
from src.helpers.log.runtime_log import RuntimeLog
from src.helpers.socket.socket_helper import SocketHelper
from src.mediators.server_mediator import ServerMediator


class ServerState:
    @staticmethod
    def run():
        log = RuntimeLog(*Config.read('main.server.log.path'))
        log.add_log('server started', 'server-state')
        log.add_log(f'listening to {Config.read("env.server.ip")}:{Config.read("env.server.port")}', 'server-state')
        sock = SocketHelper.TCPIpReusable()
        sock.bind((Config.read('env.server.ip'), Config.read('env.server.port')))
        sock.listen(5)
        try:
            log.add_log('waiting for a client', 'client-wait')
            while True:
                conn_socket, address = sock.accept()
                conn_socket.setblocking(False)
                def main():
                    log.add_log(f'client {address} connected', 'client-req')
                    try:
                        ServerMediator(sock=conn_socket, log=log) \
                            .test()
                        # ServerMediator(sock=conn_socket, log=log) \
                        #     .auth() \
                        #     .resolve_loop()
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

import socket
import select

class ChatServer:

  def __init__( self, port ):
    self.port = port
    self.srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    self.srvsock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    self.srvsock.bind( ("", port) )
    self.srvsock.listen( 5 )
    self.descriptors = [self.srvsock]    
    print ('ChatServer started on port %s' % port)

  def run( self ):
    while True:
        #Await an event on a readable socket descriptor
        (sread, swrite, sexc) = select.select(self.descriptors, [], [])
        #Iterate through the tagged read descriptors
        for sock in sread:
            #Received a connect to the server (listening) socket
            if sock == self.srvsock:
                self.accept_new_connection()
            else:
                #Received something on a client socket
                str = sock.recv(100).decode()
                #Check to see if the peer socket closed
                if str == '':
                    host,port = sock.getpeername()
                    str = 'Client left %s:%s\r\n' % (host, port)
                    self.broadcast_string( str, sock )
                    sock.close()
                    self.descriptors.remove(sock)
                else:
                    host,port = sock.getpeername()
                    newstr = '[%s:%s] %s' % (host, port, str)
                    self.broadcast_string( newstr, sock )

  def broadcast_string( self, str, omit_sock ):
    for sock in self.descriptors:
        if sock != self.srvsock and sock != omit_sock:
            sock.sendall(str.encode())
    print(str)

  def accept_new_connection( self ):
    newsock, (remhost, remport) = self.srvsock.accept()
    self.descriptors.append( newsock )

    newsock.sendall("You're connected to the Python chatserver\r\n".encode())
    str = 'Client joined %s:%s\r\n' % (remhost, remport)
    self.broadcast_string( str, newsock )
