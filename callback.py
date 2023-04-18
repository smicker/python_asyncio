"""
This demo shows how to use a callback function that is to be executed after a task returns.
(Don't really understand why you need to set default values on the arguments in get_name function
but if you do not do that pylance will complain when creating a task for that function. However,
the code will work to execute anyway.)

Printout:
    Started
    In between
    get_name started by b
    get_name started by task
    In callback: Got Kalle
    In main: Ada
    Exited
"""

import asyncio

def got_result(task):
    print(f"In callback: Got {task.result()}")

async def get_name(name="", sleep_time=3, caller=""):
    print(f"get_name started by {caller}")
    await asyncio.sleep(sleep_time)
    return name

async def main():
    print("Started")

    task = asyncio.create_task(get_name("Kalle", 2, "task"))
    task.add_done_callback(got_result)

    print("In between")

    b = await get_name("Ada", 4, "b")
    print(f"In main: {b}")

    print("Exited")

if __name__ == "__main__":
    asyncio.run(main())