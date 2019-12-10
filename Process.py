import threading
import time
from commands import calculate, io, yield_from, out, continue_from, fork
import tables


class Process:
    thread = None
    active = False
    started = False
    done = False
    lock: threading.Event = None
    dispatcher = None
    scheduler_lock = None
    pcb = None
    has_cs = False
    is_waiting_for_cs = False
    sleeping = False
    child = False

    def task(self):
        self.lock.wait()
        instruction_iterator = iter(self.program.instructions)
        instruction = next(instruction_iterator)
        while True:
            if instruction == None:
                break
            elif instruction.command == 'CALCULATE':
                calculate(instruction.value, 0.01, self.lock, self.pid)
                instruction = advance(instruction_iterator)
            elif instruction.command == 'I/O':
                io(self, self.lock, self.pid, self.dispatcher, self.scheduler_lock, self.pcb)
                instruction = advance(instruction_iterator)
            elif instruction.command == 'YIELD':
                yield_from(self.lock, self.pid, self.scheduler_lock)
                instruction = advance(instruction_iterator)
            elif instruction.command == 'OUT':
                out(self, self.lock, self.pid)
                instruction = advance(instruction_iterator)
            elif instruction.command == 'FORK':
                fork(self)
                instruction = advance(instruction_iterator)
            elif instruction.command == 'CRITICAL BEGIN':
                cs = tables.critical_sections[instruction.value]
                if not cs.locked:
                    cs.lock()
                    cs.pid = self.pid
                    self.has_cs = True
                    self.is_waiting_for_cs = False
                    instruction = advance(instruction_iterator)
                    print(f'---CRITICAL SECTION (id: {cs.id}, pid {self.pid}) BEGIN---')
                    self.lock.wait()
                elif cs.locked:
                    # print(f'Process {self.pid} waiting for lock {cs.id}')
                    self.has_cs = False
                    self.is_waiting_for_cs = True
                    self.pcb.state = 'WAIT'
                    continue_from(self.lock, self.pid, self.scheduler_lock)
            elif instruction.command == 'CRITICAL END':
                cs = tables.critical_sections[instruction.value]
                if cs.locked and cs.pid == self.pid:
                    cs.unlock()
                    cs.pid = -1
                    self.has_cs = False
                    self.is_waiting_for_cs = False
                    instruction = advance(instruction_iterator)
                    print(f'----CRITICAL SECTION (id: {cs.id}, pid {self.pid})) END----')
                    self.lock.wait()
            else:
                print(f'Invalid command: {instruction.command}')
                instruction = advance(instruction_iterator)
                self.lock.wait()
        self.pcb.state = 'DONE'
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


def advance(iterator):
    try:
        return next(iterator)
    except StopIteration:
        return None