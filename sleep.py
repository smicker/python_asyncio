"""
This demo shows that the asyncio.sleep(x) function does not say that the coroutine
will continue to execute in x seconds, but will continue to execute after at least
x seconds. After x seconds have passed the control must first be given back to
asyncio by the currently executing code, by for example calling await <task>. Then
asyncio will give the executing control back to the code that called asyncio.sleep(x).

Printout:
    Main starts
    Starting my_task
    Executing my_task
    Executing my_task
    Executing my_task
    Exiting my_task
    Exiting main
    End of program
"""

import asyncio
import time

async def my_task():
    print(f"Starting my_task")
    for _ in range(3):
        print(f"Executing my_task")
        time.sleep(1)
    print("Exiting my_task")

async def main():
    print("Main starts")

    # Schedule my_task to be executed in the future. It will not be executed
    # until main gives the control back to asyncio, which here is when it calls
    # await asyncio.sleep(0).
    task = asyncio.create_task(my_task())
    await asyncio.sleep(0)
    print("Exiting main")

asyncio.run(main())  # Blocks until main returns
print("End of program")