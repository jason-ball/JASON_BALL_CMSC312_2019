import time
import random
import tables



def calculate(count, delay, lock, pid):
    for i in range(count):
        print(f'{pid}-> CALCULATE: {i + 1}/{count}')
        time.sleep(delay)
        lock.wait()


def io(process, lock, pid, dispatcher, scheduler_lock, pcb):
    process.sleeping = True
    value = random.randint(1, 10)
    print(f'{pid}-> I/O: waiting for {value} seconds')
    if process.dispatcher is not None:
        process.dispatcher.block()
    scheduler_lock.set()
    time.sleep(value)
    process.sleeping = False
    if pcb is not None:
        pcb.state = 'READY'
    lock.wait()


def yield_from(lock, pid, scheduler_lock):
    if len(tables.ready_pcbs) > 0:
        print(f'{pid}-> YIELD')
        scheduler_lock.set()
        lock.clear()
        lock.wait()
    else:
        print(f'{pid}-> YIELD IGNORED: NO MORE PROCESSES')


def continue_from(lock, pid, scheduler_lock):
    # print(f'{pid}-> YIELD')
    scheduler_lock.set()
    lock.clear()
    lock.wait()


def out(process, lock, pid):
    print(f'--------OUT: PROCESS {pid}--------')
    print(f'Program Name: {process.program.name}')
    print(f'Instruction Count: {len(process.program.instructions)}')
    print(f'------------------------------')
    lock.wait()


def critical_begin(process, cs, lock, i, instruction):
    if not cs.locked:
        cs.lock()
        cs.pid = process.pid
        instruction = advance(i)
        print(f'---CRITICAL SECTION (id: {cs.id}, pid {process.pid}) BEGIN---')
        lock.wait()
    elif cs.locked:
        print(f'Process {process.pid} waiting for lock {cs.id}')
        continue_from(process.lock, process.pid, process.scheduler_lock)

def critical_end(process, cs, lock, i, instruction):
    if cs.locked and cs.pid == process.pid:
        cs.unlock()
        cs.pid = -1
        instruction = advance(i)
        print(f'----CRITICAL SECTION ({cs.id}, pid {process.pid})) END----')
        process.lock.wait()


def advance(iterator):
    try:
        return next(iterator)
    except StopIteration:
        return None