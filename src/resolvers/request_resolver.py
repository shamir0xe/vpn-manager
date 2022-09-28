from src.helpers.log.runtime_log import RuntimeLog
from libs.python_library.io.buffer_reader import BufferReader
from libs.python_library.io.buffer_writer import BufferWriter
from libs.python_library.io.string_buffer import StringBuffer
from src.actions.terminal.terminal_executer import TerminalExecuter
from src.models.types.server_commands import ServerCommands


class RequestResolver:
    def __init__(
        self, 
        reader: BufferReader,
        writer: BufferWriter,
        log: RuntimeLog
    ) -> None:
        self.reader = reader
        self.writer = writer
        self.log = log
    
    def do(self) -> bool:
        loop = False
        request = self.reader.next_line()[:-1]
        print(f'request is: {request}')
        parser = BufferReader(StringBuffer(request))
        command = parser.next_string()
        print(f'command is {command}')
        if command == ServerCommands.RUN_MODIFICATION.value:
            args = []
            while not parser.end_of_buffer():
                args.append(parser.next_string())
            print(f'arguments: {args}')
            TerminalExecuter.run_self(
                *args,
                log=self.log
            )
            self.writer.write_line('OK')
            loop = True
        elif command == ServerCommands.END.value:
            self.writer.write_line('OK')
        return loop
