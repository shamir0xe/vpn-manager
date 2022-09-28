from __future__ import annotations
from enum import Enum


class FlowTypes(Enum):
    NONE: FlowTypes = "none"
    CONNECTION_CHECK: FlowTypes = "connection_check"
    MODIFY: FlowTypes = "modify"
    SERVER: FlowTypes = "server"
