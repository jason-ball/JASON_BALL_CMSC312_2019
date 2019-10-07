import threading
import time


class Scheduler:
    PCBs = None
    PCBs_available = threading.Event()
    thread = None

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def run(self):
        self.PCBs_available.wait()
        for pcb in self.PCBs:
            pcb.process.start()
            pcb.state = 'READY'
        while True:
            self.PCBs[:] = [pcb for pcb in self.PCBs if not pcb.process.done]
            for pcb in self.PCBs:
                if pcb.state == 'READY':
                    self.dispatcher.switch(pcb)
                    time.sleep(2)
            if len(self.PCBs) == 0:
                break

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
