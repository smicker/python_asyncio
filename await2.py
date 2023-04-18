"""
This demo is just a small modify of await.py to show the difference of asyntio.sleep and time.sleep.

Printout:
    Main starts
    Doing stuff 2
    Starting my_work
    Executing my_work
    Executing my_work
    Exiting my_work
    Doing stuff 1
    Doing stuff 2
    Doing stuff 1
    Exiting do_stuff(2)
    Exiting do_stuff(1)
    Exiting main
    End of program
"""

import asyncio
import time

async def my_work():
    print(f"Starting my_work")
    for _ in range(2):
        print(f"Executing my_work")
        time.sleep(1)
    print("Exiting my_work")

async def do_stuff(i: int):
    for _ in range(2):
        print(f"Doing stuff {i}")
        #time.sleep(1)
        await asyncio.sleep(0)  # This is the only modification of demo await.py. This will return control to asyncio.
    print(f"Exiting do_stuff({i})")

async def main():
    print("Main starts")

    # Schedule tasks to be executed in the future. They will not be executed
    # until main gives the control back to asyncio, which here is when it calls
    # await do_stuff_task.
    my_work_task = asyncio.create_task(my_work())
    do_stuff_task = asyncio.create_task(do_stuff(1))

    # This will not give the control back to asyncio. So this would call do_stuff()
    # and wait for it to return, just like synchronous code would.
    await do_stuff(2)

    # Since do_stuff_task is a task this will give the control back to asyncio.
    # asyncio can now decide to run whatever is scheduled. In this case my_work_task
    # is scheduled first so it will be given the execution control first. When that
    # returns the asyncio is given the control back and it will then execute
    # do_stuff_task. This await will block until do_stuff_task is done.
    await do_stuff_task
    print("Exiting main")

asyncio.run(main())  # Blocks until main returns
print("End of program")