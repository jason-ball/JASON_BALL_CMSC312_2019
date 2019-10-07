# JASON_BALL_CMSC312_2019

## How to run (built using Python 3.7):
```bash
git clone https://github.com/jason-ball/JASON_BALL_CMSC312_2019.git
cd JASON_BALL_CMSC312_2019
python3 main.py
```

## Program file reference

### Example file:
```
Name: Calculator
Total runtime: 137
Memory: 45

CALCULATE 25
CALCULATE 79
I/O 57
YIELD
CALCULATE 2
I/O 4
YIELD
CALCULATE 23
CALCULATE 8
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
- `EXE` - Marks the end of the program file

