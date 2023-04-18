"""
This demo shows how to give back the control to asyncio so it can run the next scheduled task.

Printout:
    Main starts
    Starting my_task
    Back in main
    Do stuff
    Do stuff
    Exiting my_task
    Exiting main
    End of program
"""

import asyncio
import time

async def do_stuff():
    for _ in range(2):
        print("Do stuff")
        time.sleep(1)

async def my_task():
    print(f"Starting my_task")
    task2 = asyncio.create_task(do_stuff())

    # Give control back to asyncio. asyncio will continue to execute main
    await task2
    print("Exiting my_task")

async def main():
    print("Main starts")

    # Schedule my_task to be executed in the future.
    task1 = asyncio.create_task(my_task())

    # Give control back to asyncio. asyncio will execute task1
    await asyncio.sleep(0)
    print("Back in main")

    # Give control back to asyncio. asyncio will execute task2 since that is next in schedule.
    # This will block until task1 is complete.
    await task1
    print("Exiting main")

asyncio.run(main())  # Blocks until main returns
print("End of program")