from typing import NewType, Dict, List
from CriticalSection import CriticalSection
from collections import deque
from PCB import PCB
cs = NewType("CriticalSection", CriticalSection)

critical_sections = {}
PCBs = []
ready_pcbs = deque()
waiting_pcbs = deque()

memory = 4096
