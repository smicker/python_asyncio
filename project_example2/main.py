"""
Demo on how to exit task gracefully when pressing ctrl+c.
This is very close to the project_example demo but adds an event to listen to. This
is handy if you don't want to do the synchronous calls from the signal_handler to close
each task (and you probably don't want to do that if the closedown procedure is heavy).
Here you just set the event in the signal_handler and then you gracefully shut down each task
by asynchronous calls from the main task.
"""

import asyncio
import contextlib
import signal

from async_task import AsyncTask
from task1 import Task1
from task2 import Task2

QUIT: asyncio.Event = asyncio.Event()
TASK_LIST = []

def signal_handler():
    print(f"\nsig_handler: got signal ctrl+c - Exit gracefully!!")
    QUIT.set()

async def main():
    print('Main started')

    # Add signal handler (listener for ctrl+c etc)
    for sig in ('SIGINT', 'SIGTERM'):
        asyncio.get_running_loop().add_signal_handler(getattr(signal, sig), signal_handler)

    task1: AsyncTask = Task1()
    task1.set_task(asyncio.create_task(task1.run()))
    TASK_LIST.append(task1)

    task2: AsyncTask = Task2()
    task2.set_task(asyncio.create_task(task2.run()))
    TASK_LIST.append(task2)

    # Block until we exit
    while not QUIT.is_set():
        with contextlib.suppress(asyncio.TimeoutError):  # Ignore TimeoutError
            await asyncio.wait_for(QUIT.wait(), 10)

    # Close all tasks
    [await task.close("Ctrl+c pressed") for task in TASK_LIST]

    print ("Waiting for all tasks to be closed...")
    for task in TASK_LIST:
        try:
            await task.get_task()
        except asyncio.CancelledError:
            pass

    print('Main done')

asyncio.run(main())