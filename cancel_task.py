"""
Demo on how to exit task gracefully when pressing ctrl+c. If the task needs to do some cleanup work
after being closed, it shall catch the asyncio.CancelledError itself, like task1 does below. If the
task does not have to clean anything up it can just let the main loop catch the asyncio.CancelledError,
as task2 does.

Printout:
    Main started
    Task1 started
    Task2 started
    Task1 started
    Task2 started
    ^CExit gracefully!!
    Task1 received a request to cancel because of Ctrl+c pressed, cleaning up task!!
    Task1 cleaned up and exiting
    Main caught cancellederror (This will only happen for task2 since task1 catches the exception itself)
    Main done
"""

import asyncio
import signal

task_list = []

def signal_handler():
    print("Exit gracefully!!")
    [task.cancel("Ctrl+c pressed") for task in task_list]

async def task1():
    while True:
        try:
            print('Task1 started')
            await asyncio.sleep(1)
        except asyncio.CancelledError as e:
            print(f'Task1 received a request to cancel because of {e}, cleaning up task!!')
            break
    print("Task1 cleaned up and exiting")

async def task2():
    while True:
        print("Task2 started")
        await asyncio.sleep(1)
    print("Task2 cleaned up and exiting (This will never happen)")

async def main():
    print('Main started')

    for sig in ('SIGINT', 'SIGTERM'):
        asyncio.get_running_loop().add_signal_handler(getattr(signal, sig), signal_handler)

    task_list.append(asyncio.create_task(task1()))
    task_list.append(asyncio.create_task(task2()))

    try:
        [await task for task in task_list]
    except asyncio.CancelledError:
        print("Main caught cancellederror (This will only happen for task2 since task1 catches the exception itself)")

    print('Main done')

asyncio.run(main())