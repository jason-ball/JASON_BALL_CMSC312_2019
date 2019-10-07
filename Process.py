import threading
import time


class Process:
    thread = None
    active = False
    started = False
    done = False
    lock = None

    def task(self):
        self.lock.wait()
        for instruction in self.program.instructions:
            print(f'{self.pid}-> {instruction.command}: {instruction.value}')
            time.sleep(0.5)
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
