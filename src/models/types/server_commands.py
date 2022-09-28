from __future__ import annotations
from enum import Enum


class ServerCommands(Enum):
    RUN_MODIFICATION: ServerCommands = "run_modification"
    END: ServerCommands = "end"
