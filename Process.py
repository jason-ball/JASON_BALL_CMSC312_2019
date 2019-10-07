import threading
import time


class Process:
    thread = None
    active = False
    started = False
    done = False
    lock = threading.Event()

    def task(self):
        for instruction in self.program.instructions:
            self.lock.wait()
            print(f'{self.pid}-> {instruction.command}: {instruction.value}')
            time.sleep(1)
        self.done = True
        print(f'---{self.pid}: DONE---')

    def __init__(self, program, pid):
        self.program = program
        self.pid = pid
        self.thread = threading.Thread(target=self.task)

    def start(self):
        self.thread.start()
        self.started = True
