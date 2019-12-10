from Instruction import Instruction
from Program import Program
from Process import Process
from Scheduler import Scheduler
from PCB import PCB
from Dispatcher import Dispatcher
import tables
from CriticalSection import CriticalSection
from ProcessGUI import ProcessGUI
import random
import math
import copy


def main():
    program = Program()
    cs_id = 0
    random.seed()
    while True:
        try:
            filename = input("Program name: ")
            file = open(filename, 'r')
            break
        except FileNotFoundError:
            print("File not found!")
    program.number_of_processes = int(input("Number of processes: "))
    tables.memory = int(input("Memory Size: "))
    instructions = []
    for line in file:
        if line == 'EXE':
            break
        elif 'Name: ' in line:
            program.name = line.split(' ', 1)[1].splitlines()[0]
        elif 'Total runtime: ' in line:
            program.runtime = int(line.split(': ')[1])
        elif 'Memory: ' in line:
            program.memory = int(line.split(': ')[1])
        elif line != '\n':
            current_line = line.split()
            if "CRITICAL BEGIN" in line:
                begin_idx = len(instructions)
                cs = CriticalSection(cs_id, begin_idx)
                program.critical_sections.append(cs)
                tables.critical_sections[cs.id] = cs
                instructions.append(Instruction("CRITICAL BEGIN", cs_id))
                cs_id += 1
            elif "CRITICAL END" in line:
                end_idx = len(instructions)
                for cs in program.critical_sections:
                    if cs.id == cs_id - 1:
                        cs.end_idx = end_idx
                        instructions.append(Instruction("CRITICAL END", cs.id))
                        tables.critical_sections[cs.id].end_idx = end_idx
                        break
            elif len(current_line) == 1:
                instructions.append(Instruction(current_line[0], 0))
            else:
                instructions.append(Instruction(current_line[0], int(current_line[1])))
    program.instructions = instructions

    missing_end_tags = 0
    for cs in program.critical_sections:
        if cs.end_idx == -1:
            missing_end_tags += 1
    if missing_end_tags > 0:
        print(f'{missing_end_tags} critical section(s) are missing \'CRITICAL END\' commands')
        exit()

    print(f'Program loaded: {program.name}({program.number_of_processes})')

    processes = [Process(copy.deepcopy(program), pid) for pid in range(program.number_of_processes)]
    print('Randomizing...')
    for process in processes:
        # random.shuffle(process.program.instructions)
        for instruction in\
                (instruction for instruction in process.program.instructions if instruction.command == 'CALCULATE'):
            instruction.value = random.randint(math.floor(instruction.value / 2), instruction.value * 2)
    pcbs = [PCB(process) for process in processes]
    for pcb in pcbs:
        pcb.process.pcb = pcb

    for pcb in pcbs:
        print(f'------Process {pcb.process.pid}------')
        for instruction in pcb.process.program.instructions:
            print(f'{instruction.command}: {instruction.value}')
        print(f'---------------------')
    input('Press enter/return to start execution...')


    dispatcher = Dispatcher()
    scheduler = Scheduler(dispatcher)
    dispatcher.connect_scheduler(scheduler)
    scheduler.start()
    tables.PCBs = pcbs
    scheduler.pcb_lock.set()

    gui = ProcessGUI()
    # gui.start()

    scheduler.run_thread.join()

if __name__ == '__main__':
    main()
