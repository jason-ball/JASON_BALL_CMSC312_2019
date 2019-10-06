import threading


class Process:
    thread = None
    active = False
    started = False

    def task(self):
        print(self.program.name)

    def __init__(self, program):
        self.program = program
        self.thread = threading.Thread(target=self.task)

    def start(self):
        self.thread.start()
        self.started = True
