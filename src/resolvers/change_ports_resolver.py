from typing import Tuple, Union
from src.actions.server.authentication import Authentication
from src.actions.terminal.terminal_executer import TerminalExecuter
from src.resolvers.resolver import Resolver
from src.data_transfers.change_ports_data import ChangePortsData


class ChangePortsResolver(Resolver):
    def resolve(self) -> Tuple[bool, Union[dict, str]]:
        data = ChangePortsData(self.request.json).get()
        if not Authentication.check_token(data.token):
            return (False, 'invalid token')
        print('valid token')
        print('data received: %s' % data)
        out, err = TerminalExecuter.run_self(
            '--gate', 
            '--interface.port', data.interface_port, 
            '--peer.port', data.peer_port,
        )
        print('outputs: ', out + err)
        if err != '':
            return (False, err)
        return (True, 'job started')
        