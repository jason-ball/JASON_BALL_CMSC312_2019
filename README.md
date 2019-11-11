# JASON_BALL_CMSC312_2019

## How to run (built using Python 3.7):
```bash
git clone https://github.com/jason-ball/JASON_BALL_CMSC312_2019.git
cd JASON_BALL_CMSC312_2019
python3 main.py
# You'll then be asked to enter the program file's name,
# number of processes, and total memory needed
```

## Program file reference

### Example file:
```
Name: Calculator
Total runtime: 137
Memory: 45

CALCULATE 25
CALCULATE 79
CRITICAL BEGIN
YIELD
CALCULATE 2
CRITICAL END
I/O 57
I/O 4
YIELD
CRITICAL BEGIN
CALCULATE 23
CALCULATE 8
CRITICAL END
OUT
I/O 8
EXE
```

### Header
```
Name: <Name of the program>
Total runtime: <Number of needed CPU cycles>
Memory: <Amount of memory needed for execution>
```

### Commands
- `CALCULATE` - Runs for the given number of cycles
- `I/O` - Places the process in a blocked state for a random number of cycles
- `YIELD` - Yields control back to the scheduler
- `OUT` - Prints basic information about the process
- `CRITICAL BEGIN` - Marks the beginning of a critical section
- `CRITICAL END` - Marks the end of a critical section
- `EXE` - Marks the end of the program file

### Process GUI

![Process GUI Screenshot](https://cdn.jasonball.cloud/project/ProcessGUI.png)

__Note for macOS:__ The version of Python and Tkinter supplied by Apple is __not__ compatible with the process GUI. You can download the latest version [here](https://www.python.org/downloads/mac-osx/). 

- Process states in blue are currently in a critical section.
- Process states in red are waiting to enter a critical secion.
- __NOTE:__ The simulator will not exit until the GUI window is closed!