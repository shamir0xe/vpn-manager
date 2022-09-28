from __future__ import annotations
import subprocess
import shlex
from src.helpers.log.runtime_log import RuntimeLog


class SingleProcess:
    def __init__(self, *args, **kwargs) -> None:
        self.log = None
        if 'log' in kwargs and isinstance(kwargs['log'], RuntimeLog):
            self.log = kwargs['log']
        args = [arg if isinstance(arg, str) else str(arg) for arg in args]
        self.command = ' '.join(args)
        if self.log:
            self.log.add_log('%s' % self.command, 'terminal')

    def run(self) -> SingleProcess:
        self.proc = subprocess.Popen(
            shlex.split(self.command), 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        )
        return self
    
    def communicate(self, input: str = None) -> str:
        stdout, stderr =  self.proc.communicate(input=input)
        return (self.stringify(stdout), self.stringify(stderr))

    @staticmethod
    def stringify(buffer) -> str:
        if buffer is None:
            return ''
        res = ''
        for line in buffer:
            res += line
        return res

    def output(self) -> str:
        out = ''
        first = True
        while True:
            line = self.proc.stdout.readline().decode('utf-8')
            if not line:
                break
            if first:
                first = False
            else:
                out += '\n'
            out += line.rstrip()
        return out
    