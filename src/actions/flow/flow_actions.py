from src.helpers.config.config import Config
from src.actions.node.node_actions import NodeActions
from src.helpers.argument.argument_parser import ArgumentParser
from src.models.types.flow_types import FlowTypes


class FlowActions:
    @staticmethod
    def detect_flow() -> FlowTypes:
        flow = FlowTypes.NONE
        if ArgumentParser.is_option('connection_check') and \
            not NodeActions.access_youtube():
            flow = FlowTypes.CONNECTION_CHECK
        elif ArgumentParser.is_option('server'):
            flow = FlowTypes.SERVER
        elif ArgumentParser.is_option(Config.read('main.middleman.name')) or ArgumentParser.is_option(Config.read('main.gate.name')):
            flow = FlowTypes.MODIFY
        return flow
