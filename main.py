from src.models.types.flow_types import FlowTypes
from src.actions.flow.flow_actions import FlowActions
from src.states.modify_state import ModifyState
from src.states.server_state import ServerState

def main():
    flow = FlowActions.detect_flow()
    print(flow)
    if flow is FlowTypes.CONNECTION_CHECK or flow is FlowTypes.MODIFY:
        ModifyState.run(flow)
    elif flow is FlowTypes.SERVER:
        ServerState.run()

if __name__ == '__main__':
    main()
