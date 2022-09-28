from __future__ import annotations
from enum import Enum


class NodeTypes(Enum):
    GATE: NodeTypes = "gate"
    MIDDLEMAN: NodeTypes = "middleman"
