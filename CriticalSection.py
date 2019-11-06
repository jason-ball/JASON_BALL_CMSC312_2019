class CriticalSection:
    locked = False
    pid = -1

    def __init__(self, id, begin_idx, end_idx=-1):
        self.id = id
        self.begin_idx = begin_idx
        self.end_idx = end_idx
    
    def lock(self):
        self.locked = True

    
    def unlock(self):
        self.locked = False

