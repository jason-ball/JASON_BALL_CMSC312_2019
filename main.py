from Instruction import Instruction
from Program import Program


def main():
    program = Program()
    while True:
        try:
            filename = input("Program name: ")
            file = open(filename, 'r')
            break
        except FileNotFoundError:
            print("File not found!")
    program.threads = int(input("Number of threads: "))
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
            instructions.append(Instruction(current_line[0], int(current_line[1])))
    program.instructions = instructions

    print(f'Program loaded: {program.name}({program.threads})')

    for itr in program.instructions:
        print(f'{itr.command}: {itr.value}')


if __name__ == '__main__':
    main()
