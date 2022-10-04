from multiprocessing import Process
from wsgiref.simple_server import server_version
from libs.python_library.config.config import Config
from src.helpers.log.runtime_log import RuntimeLog
from src.helpers.socket.socket_helper import SocketHelper
from src.mediators.server_mediator import ServerMediator
import socketserver
from bottle import route, run, template, request
import sys


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/login', method='POST')
def login():
    print(request.json)
    username, password = (request.json['username'], request.json['password'])
    request.content_type = 'application/json'
    print(f'usr: {username}, pass: {password}')
    if username == 'test' and password == 123:
        return '''
        {
            "status": true,
            "message": "ok"
        }
        '''
    else:
        return '''
        {
            "status": false,
            "message": "wrong credentials"
        }
        '''

class ServerState:
    @staticmethod
    def run():
        host, port = (Config.read('env.server.ip'), Config.read('env.server.port'))
        run(host=host, port=port, debug=True)
        # socketserver.TCPServer.allow_reuse_address = True
        # with socketserver.TCPServer((host, port), RequestHandler) as server:
        #     print(f'starting the server on ({host}, {port})')
        #     server.serve_forever()
        # log = RuntimeLog(*Config.read('main.server.log.path'))
        # log.add_log('server started', 'server-state')
        # log.add_log(f'listening to {Config.read("env.server.ip")}:{Config.read("env.server.port")}', 'server-state')
        # sock = SocketHelper.TCPIpReusable()
        # sock.bind((Config.read('env.server.ip'), Config.read('env.server.port')))
        # sock.listen(5)
        # try:
        #     log.add_log('waiting for a client', 'client-wait')
        #     while True:
        #         conn_socket, address = sock.accept()
        #         conn_socket.setblocking(False)
        #         def main():
        #             log.add_log(f'client {address} connected', 'client-req')
        #             try:
        #                 ServerMediator(sock=conn_socket, log=log) \
        #                     .test()
        #                 # ServerMediator(sock=conn_socket, log=log) \
        #                 #     .auth() \
        #                 #     .resolve_loop()
        #             except BaseException as err:
        #                 log.add_log(f'error: {err}', 'runtime-error')
        #             return 0
        #         process = Process(target=main)
        #         process.start()
        #         process.join(Config.read('main.connection.total_timeout'))
        #         process.terminate()
        #         if process.exitcode is None:
        #             log.add_log('error: timeout', 'main-server')
        #         conn_socket.close()
        #         log.add_log('\nwaiting for a client', 'client-wait')
        # except BaseException as err:
        #     log.add_log(f'error: {err}', 'main-server')
        # finally:
        #     sock.shutdown(1)
        #     sock.close()

class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print(self.client_address)
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())
