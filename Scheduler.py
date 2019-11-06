import threading
import time
import tables


class Scheduler:
    PCBs = tables.PCBs
    PCBs_available = threading.Event()
    thread = None
    wait_lock = threading.Event()

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def run(self):
        self.PCBs_available.wait()
        for pcb in tables.PCBs:
            pcb.process.start()
            pcb.process.scheduler_lock = self.wait_lock
            pcb.process.dispatcher = self.dispatcher
            pcb.state = 'READY'
        while True:
            self.wait_lock.clear()
            # tables.PCBs[:] = [pcb for pcb in tables.PCBs if not pcb.process.done]
            # for pcb in tables.PCBs:
            for pcb in [pcb for pcb in tables.PCBs if not pcb.process.done]:
                if pcb.state == 'READY':
                    self.dispatcher.switch(pcb)
                    self.wait_lock.wait(1)
            if len([pcb for pcb in tables.PCBs if not pcb.process.done]) == 0:
                break

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
