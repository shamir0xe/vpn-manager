from libs.python_library.argument.argument_parser import ArgumentParser
from src.mediators.app_mediator import App
from src.models.types.flow_types import FlowTypes
from src.actions.node.node_actions import NodeActions


class ModifyState:
    @staticmethod
    def run(flow: FlowTypes) -> None:
        import socket
        import time

        HOST = '127.0.0.1'        # The remote host
        # HOST = 'zimbo.app'        # The remote host
        PORT = 50007              # The same port as used by the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            while True:
                s.sendall(b'Hello, world')
                data = s.recv(1024)
                if not data:
                    break
                print('Received', repr(data))
                time.sleep(1)
        return

        app = None
        node_type = NodeActions.extract_type()
        app = App(node_type=node_type, flow=flow) \
            .add_log('\n') \
            .add_log(f'start of the {node_type.value} process')
        if ArgumentParser.is_option('debug'):
            # debug
            app \
                .read_local_config() \
                .apply_arguments_config() \
                .apply_env() \
                .send_changes_to_gates()
            return
        # main part
        app \
            .down_vpn() \
            .read_local_config() \
            .remove_previous_ufw() \
            .apply_arguments_config() \
            .change_port() \
            .apply_local_config() \
            .apply_env() \
            .build_template() \
            .save() \
            .add_new_ufw() \
            .reset_ufw_service() \
            .send_changes_to_gates() \
            .up_vpn()
        # log part
        app \
            .telegram_broadcast() \
            .add_log('end of the process') \
            .closure()
