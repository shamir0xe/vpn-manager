from libs.python_library.argument.argument_parser import ArgumentParser
from src.mediators.app_mediator import App
from src.models.types.flow_types import FlowTypes
from src.actions.node.node_actions import NodeActions


class ModifyState:
    @staticmethod
    def run(flow: FlowTypes) -> None:
        import socket
        import time
        from libs.python_library.io.buffer_reader import BufferReader
        from libs.python_library.io.buffer_writer import BufferWriter
        from src.helpers.socket.socket_buffer import SocketBuffer

        # HOST = '127.0.0.1'   # The remote host
        HOST = '185.235.40.240'   # The remote host
        snd_port = 50081         
        rec_port = 50080
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect((HOST, PORT))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, snd_port))
            s.sendall(b'Hello, world')
            data = s.recv(1024)
        print('Received', repr(data))

        # writer, reader = BufferWriter(SocketBuffer(s)), BufferReader(SocketBuffer(s))
        # while True:
        #     writer.write_line('Hello, cruel world')
        #     try:
        #         data = reader.next_line()
        #         print('Received', data.strip())
        #         time.sleep(1)
        #     except BaseException as err:
        #         print(f'err: {err}')
        #         break
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
