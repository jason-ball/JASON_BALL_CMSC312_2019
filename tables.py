from typing import NewType, Dict
from CriticalSection import CriticalSection
cs = NewType("CriticalSection", CriticalSection)

critical_sections = {}
PCBs = []
