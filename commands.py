import time
import random


def calculate(count, delay, lock, pid):
    for i in range(count):
        print(f'{pid}-> CALCULATE: {i + 1}/{count}')
        time.sleep(delay)
        lock.wait()


def io(lock, pid, dispatcher, scheduler_lock, pcb):
    value = random.randint(0, 10)
    print(f'{pid}-> I/O: waiting for {value} seconds')
    if dispatcher is not None:
        dispatcher.block()
    scheduler_lock.set()
    time.sleep(value)
    if pcb is not None:
        pcb.state = 'READY'
    lock.wait()


def yield_from(lock, pid, scheduler_lock):
    print(f'{pid}-> YIELD')
    scheduler_lock.set()
    # lock.clear()
    lock.wait()


def continue_from(lock, pid, scheduler_lock):
    # print(f'{pid}-> YIELD')
    scheduler_lock.set()
    # lock.clear()
    lock.wait()


def out(process, lock, pid):
    print(f'--------OUT: PROCESS {pid}--------')
    print(f'Program Name: {process.program.name}')
    print(f'Instruction Count: {len(process.program.instructions)}')
    print(f'------------------------------')
    lock.wait()
