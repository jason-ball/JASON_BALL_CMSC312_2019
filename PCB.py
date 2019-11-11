class PCB:
    state = 'NEW'
    process = None

    def __init__(self, process):
        self.process = process
        self.memory = process.program.memory
