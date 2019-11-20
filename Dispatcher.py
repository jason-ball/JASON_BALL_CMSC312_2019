from PCB import PCB
import tables
from threading import Thread, Event
from time import sleep

class Dispatcher:
    def __init__(self):
        self.pcb: PCB = None
        self.run_thread: Thread = Thread(target=self.run)
        self.done = False


    def connect_scheduler(self, scheduler):
        self.scheduler = scheduler
    

    def submit(self, pcb: PCB):
        if self.pcb is not None:
            self.pcb.process.lock.clear()
            if self.pcb.state == 'DONE':
                tables.memory += self.pcb.memory
                self.scheduler.schedule()
            elif self.pcb.state == 'WAIT':
                tables.waiting_pcbs.appendleft(self.pcb)
            else:
                self.pcb.state = 'READY'
                tables.ready_pcbs.appendleft(self.pcb)
        self.pcb = pcb
        self.pcb.state = 'RUN'
        self.pcb.process.dispatcher = self
        self.pcb.process.lock.set()
    

    def clear(self):
        if self.pcb is not None:
            self.pcb.process.lock.clear()
            self.pcb = None


    def block(self):
        self.pcb.state = 'WAIT'
        self.pcb.process.lock.clear()
        if self.scheduler is not None:
            self.scheduler.run_lock.set()


    def run(self):
        while self.done:
            if self.pcb is not None:
                self.pcb.process.lock.set()
                sleep(1)


    def done_waiting(self):
        if self.scheduler is not None:
            self.scheduler.schedule()
