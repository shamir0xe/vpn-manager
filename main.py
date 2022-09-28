from src.models.types.flow_types import FlowTypes
from src.actions.flow.flow_actions import FlowActions
from src.states.modify_state import ModifyState
from src.states.server_state import ServerState

def main():
    """
    three main functionality porovided:
        1) --server
            creating a server and binding {env.port} to it
        2) --middleman --connection_check (set properties)
            if interface doesnt have access to desire website,
            it will try to change it's config and send new-
            config to gates
        3) (--gate|--middleman) (set properties)
            changing current config of the node, and send
            final config to gates
    """
    flow = FlowActions.detect_flow()
    print(flow)
    if flow is FlowTypes.CONNECTION_CHECK or flow is FlowTypes.MODIFY:
        ModifyState.run(flow)
    elif flow is FlowTypes.SERVER:
        ServerState.run()

if __name__ == '__main__':
    main()
