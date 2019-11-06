class Dispatcher:
    active_pcb = None

    def switch(self, pcb):
        if self.active_pcb is not None:
            self.active_pcb.process.lock.clear()
            self.active_pcb.dispatcher = None
            if self.active_pcb.state != 'DONE' and not self.active_pcb.process.sleeping:
                self.active_pcb.state = 'READY'
        self.active_pcb = pcb
        self.active_pcb.dispatcher = self
        self.active_pcb.process.lock.set()
        self.active_pcb.state = 'RUN'

    def clear(self):
        if self.active_pcb is not None:
            self.active_pcb.process.lock.clear()
            self.active_pcb = None

    def block(self):
        self.active_pcb.state = 'WAIT'
        self.active_pcb.process.lock.clear()
