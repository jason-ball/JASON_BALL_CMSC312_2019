from Instruction import Instruction
from Program import Program
from Process import Process
from Scheduler import Scheduler
from PCB import PCB
from Dispatcher import Dispatcher
import random
import math
import copy


def main():
    program = Program()
    while True:
        try:
            filename = input("Program name: ")
            file = open(filename, 'r')
            break
        except FileNotFoundError:
            print("File not found!")
    program.number_of_processes = int(input("Number of processes: "))
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
            if len(current_line) == 1:
                instructions.append(Instruction(current_line[0], 0))
            else:
                instructions.append(Instruction(current_line[0], int(current_line[1])))
    program.instructions = instructions

    print(f'Program loaded: {program.name}({program.number_of_processes})')

    # for itr in program.instructions:
    #     print(f'{itr.command}: {itr.value}')

    processes = [Process(copy.deepcopy(program), pid) for pid in range(program.number_of_processes)]
    print('Randomizing...')
    for process in processes:
        random.seed()
        random.shuffle(process.program.instructions)
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
    scheduler.start()
    scheduler.PCBs = pcbs
    scheduler.PCBs_available.set()

    scheduler.thread.join()


if __name__ == '__main__':
    main()
