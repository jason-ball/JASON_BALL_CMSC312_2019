import threading
import time
import tables
from time import sleep
from PCB import PCB
from Dispatcher import Dispatcher

class Scheduler:
    def __init__(self, dispatcher: Dispatcher):
        self.dispatcher = dispatcher
        # self.schedule_thread = threading.Thread(target=self.schedule)
        # self.schedule_lock = threading.Event()
        # self.schedule_lock.set()
        self.run_thread = threading.Thread(target=self.run)
        self.run_lock = threading.Event()
        self.pcb_lock = threading.Event()
    

    def start(self):
        print("Scheduler Starting!")
        # self.schedule_thread.start()
        self.run_thread.start()


    def schedule(self):
        # Schedule waiting processes:
        for pcb in [pcb for pcb in tables.waiting_pcbs]:
            if pcb.process.sleeping == False or pcb.process.is_waiting_for_cs == False:
                tables.ready_pcbs.appendleft(pcb)
                tables.ready_pcbs[0].state = 'READY'
                tables.waiting_pcbs.remove(pcb)


        # Schedule new processes
        for pcb in [p for p in tables.PCBs if p.state == 'NEW']:
            if pcb.memory < tables.memory:
                tables.memory -= pcb.memory
                pcb.state = 'READY'
                pcb.process.start()
                pcb.process.scheduler_lock = self.run_lock
                tables.ready_pcbs.appendleft(pcb)
            else:
                break
    

    def run(self):
        self.pcb_lock.wait()
        self.schedule()

        while len(tables.ready_pcbs) != 0 or len(tables.waiting_pcbs) != 0:
            if len(tables.ready_pcbs) <= 1 and (len(tables.waiting_pcbs) > 0 or len([x for x in tables.PCBs if x == 'NEW'])):
                self.schedule()
            self.run_lock.clear()
            self.dispatcher.submit(tables.ready_pcbs.pop())
            self.run_lock.wait(1)
