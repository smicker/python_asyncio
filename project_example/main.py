"""
Demo on how to exit task gracefully when pressing ctrl+c.
"""

import asyncio
import signal

from async_task import AsyncTask
from task1 import Task1
from task2 import Task2

TASK_LIST = []

def signal_handler():
    print("Exit gracefully!!")
    [task.close("Ctrl+c pressed") for task in TASK_LIST]

async def main():
    print('Main started')

    for sig in ('SIGINT', 'SIGTERM'):
        asyncio.get_running_loop().add_signal_handler(getattr(signal, sig), signal_handler)

    task1: AsyncTask = Task1()
    task1.set_task(asyncio.create_task(task1.run()))
    TASK_LIST.append(task1)

    task2: AsyncTask = Task2()
    task2.set_task(asyncio.create_task(task2.run()))
    TASK_LIST.append(task2)

    for task in TASK_LIST:
        try:
            await task.get_task()
        except asyncio.CancelledError:
            pass

    print('Main done')

asyncio.run(main())