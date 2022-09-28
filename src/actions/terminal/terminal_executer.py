from libs.python_library.path.path import Path
from src.helpers.log.runtime_log import RuntimeLog
from src.models.types.node_types import NodeTypes
from src.helpers.terminal.single_process import SingleProcess
from libs.python_library.json.json_helper import JsonHelper
from libs.python_library.config.config import Config


class TerminalExecuter:
    @staticmethod
    def allow_interface_port(config: dict, node_type: NodeTypes, log: RuntimeLog = None) -> tuple:
        out, err = SingleProcess(
            "sudo",
            *Config.read(f'main.{node_type.value}.commands.ufw.allow'),
            JsonHelper.selector_get_value(config, 'interface.port'),
            log=log
        ).run().communicate()
        if log:
            log.add_log(out + err, 'allow-interface-port')
        return (out, err)

    @staticmethod
    def allow_peer_port(config: dict, node_type: NodeTypes, log: RuntimeLog = None) -> str:
        out, err = SingleProcess(
            "sudo",
            *Config.read(f'main.{node_type.value}.commands.ufw.allow'),
            JsonHelper.selector_get_value(config, 'peer.port'),
            log=log
        ).run().communicate()
        if log:
            log.add_log(out + err, 'allow-peer-port')
        return (out, err)

    @staticmethod
    def restart_ufw(node_type: NodeTypes, log: RuntimeLog = None) -> str:
        out, err = SingleProcess(
            "sudo",
            *Config.read(f'main.{node_type.value}.commands.systemctl.ufw.restart'),
            log=log
        ).run().communicate()
        if log:
            log.add_log(out + err, 'restart-ufw')
        return (out, err)

    @staticmethod
    def remove_interface_port(config: dict, node_type: NodeTypes, log: RuntimeLog = None) -> str:
        out, err = SingleProcess(
            "sudo",
            *Config.read(f'main.{node_type.value}.commands.ufw.delete'),
            JsonHelper.selector_get_value(config, 'interface.port'),
            log=log
        ).run().communicate()
        if log:
            log.add_log(out + err, 'remove-interface-port')
        return (out, err)
    
    @staticmethod
    def remove_peer_port(config: dict, node_type: NodeTypes, log: RuntimeLog = None) -> str:
        out, err = SingleProcess(
            "sudo",
            *Config.read(f'main.{node_type.value}.commands.ufw.delete'),
            JsonHelper.selector_get_value(config, 'peer.port'),
            log=log
        ).run().communicate()
        if log:
            log.add_log(out + err, 'remove-peer-port')
        return (out, err)

    @staticmethod
    def vpn_up(node_type: NodeTypes, log: RuntimeLog = None) -> str:
        out, err = SingleProcess(
            "sudo",
            Config.read(f'main.{node_type.value}.commands.up'),
            log=log
        ).run().communicate()
        if log:
            log.add_log(out + err, 'vpn-up')
        return (out, err)

    @staticmethod
    def vpn_down(node_type: str, log: RuntimeLog = None) -> str:
        out, err = SingleProcess(
            "sudo",
            Config.read(f'main.{node_type.value}.commands.down'),
            log=log
        ).run().communicate()
        if log:
            log.add_log(out + err, 'vpn-down')
        return (out, err)
    
    @staticmethod
    def run_self(*args, **kwargs) -> str:
        log = None
        if 'log' in kwargs:
            log = kwargs['log']
        out, err = SingleProcess(
            "sudo",
            Config.read('main.general.python_interpreter'), 
            Path.from_root('main.py'),
            *args,
            log=log
        ).run().communicate()
        if log:
            log.add_log(out + err, 'run-self-script')
        return (out, err)
