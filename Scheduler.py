import threading
import time


class Scheduler:
    PCBs = None
    PCBs_available = threading.Event()
    thread = None

    def run(self):
        self.PCBs_available.wait()
        for pcb in self.PCBs:
            pcb.process.start()
            pcb.process.thread.join()
            time.sleep(2)

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
