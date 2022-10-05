from bottle import Bottle, request, response
from src.resolvers.login_resolver import LoginResolver
from src.resolvers.change_ports_resolver import ChangePortsResolver


middleman_app = Bottle()

@middleman_app.route('/login', method='POST')
def login():
    return LoginResolver(request, response).do()

@middleman_app.route('/change_ports', method='POST')
def change_ports():
    return ChangePortsResolver(request, response).do()
