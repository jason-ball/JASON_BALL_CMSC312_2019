import threading
import time
from commands import calculate, io, yield_from, out


class Process:
    thread = None
    active = False
    started = False
    done = False
    lock = None
    dispatcher = None
    scheduler_lock = None
    pcb = None

    def task(self):
        self.lock.wait()
        for instruction in self.program.instructions:
            if instruction.command == 'CALCULATE':
                calculate(instruction.value, 0.01, self.lock, self.pid)
            elif instruction.command == 'I/O':
                io(self.lock, self.pid, self.dispatcher, self.scheduler_lock, self.pcb)
            elif instruction.command == 'YIELD':
                yield_from(self.lock, self.pid, self.scheduler_lock)
            elif instruction.command == 'OUT':
                out(self, self.lock, self.pid)
            else:
                print(f'Invalid command: {instruction.command}')
                self.lock.wait()
        self.done = True
        print(f'---{self.pid}: DONE---')

    def __init__(self, program, pid):
        self.program = program
        self.pid = pid
        self.thread = threading.Thread(target=self.task)
        self.lock = threading.Event()

    def start(self):
        self.thread.start()
        self.started = True
