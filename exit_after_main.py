"""
asyncio.run(main()) will create the asyncio loop and start the task main().
main will create two tasks and schedule them to be executed in the future (when
control is given back to asyncio).
Then main returns and that will give back the control to asyncio. asyncio now has
two scheduled tasks to be executed and it will start with the first one. When the
first task reaches await asyncio.sleep(1) it will give control back to asyncio.
asyncio will then start the second task. When the second task reaches
await asyncio.sleep(1) it will give back control to asyncio. asyncio no longer has
any scheduled tasks to run as the main task has returned. asyncio will then
terminate the asyncio loop. The effect is that the tasks, that waits for
asyncio.sleep(1) is terminated and will not continue to run, so "Exiting my_task"
will never be printed.

Note that if the tasks would NOT have called asyncio.sleep(1), to give the control
back to asyncio, the "while True" loop in the tasks would have executed forever.

Printout:
    Main starts
    Exiting main
    Starting my_task 1
    Executing my_task 1
    Starting my_task 2
    Executing my_task 2
    End of program
"""

import asyncio

async def my_task(i: int):
    print(f"Starting my_task {i}")
    while True:
        print(f"Executing my_task {i}")
        await asyncio.sleep(1)
        print("Exiting my_task")

async def main():
    print("Main starts")

    # Schedule my_task to be executed in the future. It will not be executed
    # until main gives the control back to asyncio, which here is when it ends.
    task = asyncio.create_task(my_task(1))
    task = asyncio.create_task(my_task(2))
    print("Exiting main")

asyncio.run(main())  # Blocks until main returns
print("End of program")