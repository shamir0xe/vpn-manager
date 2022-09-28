from __future__ import annotations
import json
from libs.python_library.file.file import File
from libs.python_library.argument.argument_parser import ArgumentParser
from libs.python_library.path.path import Path
from libs.python_library.config.config import Config
from libs.python_library.json.json_helper import JsonHelper
from src.models.types.flow_types import FlowTypes
from src.actions.node.node_actions import NodeActions
from src.models.types.node_types import NodeTypes
from src.actions.terminal.terminal_executer import TerminalExecuter
from src.helpers.log.runtime_log import RuntimeLog
from src.builders.extension_builder import ExtensionBuilder
from src.mediators.client_mediator import ClientMediator


class App:
    def __init__(self, node_type: NodeTypes, flow: FlowTypes) -> None:
        self.node_type = node_type
        self.flow = flow
        self.peer_type = NodeActions.extract_peer_type()
        self.status = True
        self.template = None
        self.__log = RuntimeLog(*Config.read(f'main.{node_type.value}.log.path'))
        
    def add_log(self, *args) -> App:
        self.__log.add_log(*args)
        return self

    def down_vpn(self) -> App:
        if not self.status:
            return self
        TerminalExecuter.vpn_down(self.node_type, self.__log)
        return self

    def up_vpn(self) -> App:
        if not self.status:
            return self
        TerminalExecuter.vpn_up(self.node_type, self.__log)
        return self

    def remove_previous_ufw(self) -> App:
        if not self.status:
            return self
        TerminalExecuter.remove_interface_port(self.config_json, self.node_type, self.__log)
        TerminalExecuter.remove_peer_port(self.config_json, self.node_type, self.__log)
        return self
    
    def add_new_ufw(self) -> App:
        if not self.status:
            return self
        TerminalExecuter.allow_interface_port(self.config_json, self.node_type, self.__log)
        TerminalExecuter.allow_peer_port(self.config_json, self.node_type, self.__log)
        return self
    
    def reset_ufw_service(self) -> App:
        if not self.status:
            return self
        TerminalExecuter.restart_ufw(self.node_type, self.__log)
        return self
    
    def read_local_config(self) -> App:
        if not self.status:
            return self
        self.config_json = Config.read(f'{self.node_type.value}.data')
        return self
    
    def apply_arguments_config(self) -> App:
        modifiables = list(set(Config.read(f'{self.node_type.value}.order')))
        for option in ArgumentParser.get_options():
            option = str.lower(option)
            if option in modifiables:
                self.config_json = JsonHelper.selector_set_value(
                    self.config_json,
                    option,
                    ArgumentParser.get_value(option)[0]
                )
        return self
    
    def change_port(self) -> App:
        """
        change port of the interface based on app flow
        """
        if not self.status:
            return self
        if self.flow is FlowTypes.CONNECTION_CHECK:
            new_port = NodeActions.random_port()
            self.config_json = JsonHelper.selector_set_value(
                self.config_json,
                'peer.port',
                new_port
            )
            self.add_log(f'new port: {new_port}', 'change-port')
        return self
    
    def apply_local_config(self) -> App:
        """
        change local config and save it to configs/*.json
        """
        if not self.status:
            return self
        node_config = Config.read(f'{self.node_type.value}')
        node_config = JsonHelper.selector_set_value(
            node_config,
            'data',
            self.config_json
        )
        try:
            File.write_file(
                Path.from_root(
                    *Config.read(f'main.{self.node_type.value}.node_config_path')
                ),
                json.dumps(node_config)
            )
            self.add_log('applied succesfully', 'apply-local-config')
        except BaseException as err:
            self.status = False
            self.add_log(f'error happened: {err}', 'apply-local-config')
        return self
    
    def apply_env(self) -> App:
        """
        apply env variables to constructed config
        """
        if not self.status:
            return self
        env = Config.read('env')
        self.config_json = JsonHelper.selector_set_value(
            self.config_json,
            'interface.private_key',
            JsonHelper.selector_get_value(env, f'{self.node_type.value}.private_key')
        )
        self.config_json = JsonHelper.selector_set_value(
            self.config_json,
            'peer.public_key',
            JsonHelper.selector_get_value(env, f'{self.peer_type.value}.public_key')
        )
        self.config_json = JsonHelper.selector_set_value(
            self.config_json,
            'peer.ip',
            JsonHelper.selector_get_value(env, f'{self.peer_type.value}.ip')
        )
        return self

    def build_template(self) -> App:
        """
        apply constructed config to the respective template
        """
        if not self.status:
            return self
        self.template = None
        try:
            self.template = ExtensionBuilder(
                node_type=self.node_type, 
                config=self.config_json, 
                log=self.__log
            ) \
                .append_core() \
                .append_before() \
                .append_after() \
                .get_template()
        except BaseException as err:
            self.add_log(f'error: {err}', 'reading-template')
            self.status = False
        print(self.template)
        return self

    def save(self) -> App:
        """
        save it to the main config file
        """
        try:
            File.write_file(Config.read(f'main.{self.node_type.value}.config.path'), self.template)
        except BaseException as err:
            self.add_log(f'error: {err}', 'save-config')
            self.status = False
            return self
        return self
    
    def send_changes_to_gates(self) -> App:
        if not self.status:
            return self
        if self.node_type is NodeTypes.GATE:
            return self
        # node type is MIDDLEMAN
        ClientMediator(log=self.__log) \
            .check_network() \
            .login() \
            .request_modification(
                port=JsonHelper.selector_get_value(
                    self.config_json, 
                    'interface.port'
                ),
                gate_port=JsonHelper.selector_get_value(
                    self.config_json,
                    'peer.port'
                )
            ) \
            .request_end() \
            .close()
        return self

    def closure(self) -> App:
        self.__log.close()
        return self
    
    def telegram_broadcast(self) -> App:
        if not self.status:
            return self
        return self
