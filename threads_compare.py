"""
Demo that shows the benifit of using thread execution (eg. run_in_executor) for things that
cannot run non-blocking.

This example is of course silly because there is asyncio.sleep() that suspends a coroutine
without spending a slot in a thread pool, but it shows the basic idea. Realistic use cases
for run_in_executor include:

- integrating CPU-bound code, such as numpy or pandas calculations, into an asyncio program.
- invoking legacy code that hasn't yet been ported to asyncio.
- blocking calls where non-blocking APIs are simply unavailable - e.g. proprietary database
  drivers, or blocking OS-level calls such as those for file system access.

Printout:
    First test with threads:
    going to sleep (thread)
    going to sleep (thread)
    waking up 5
    waking up 5

    Second test without threads:
    going to sleep (not thread)
    waking up 3
    going to sleep (not thread)
    waking up 3

    Third test with tasks:
    going to sleep (not thread)
    waking up 3
    going to sleep (not thread)
    waking up 3

    Forth test with tasks:
    going to sleep (thread)
    going to sleep (thread)
    waking up 5
    waking up 5

    Fifth test with tasks:
    going to sleep (thread)
    waking up 5
    going to sleep (thread)
    waking up 5
"""

import asyncio
import time

def sleeper(time_to_sleep):
    time.sleep(time_to_sleep)
    return time_to_sleep

async def sleep_test_different_threads():
    print('going to sleep (thread)')
    loop = asyncio.get_event_loop()
    a = await loop.run_in_executor(None, sleeper, 5)  # Gives control back to asyncio event loop
    print(f'waking up {a}')

async def sleep_test_same_thread():
    print('going to sleep (not thread)')
    a = sleeper(3)
    print(f'waking up {a}')

async def main():
    print("First test with threads:")
    # runs two sleep tests in parallel and wait until both finish
    await asyncio.gather(sleep_test_different_threads(), sleep_test_different_threads())

    print("\nSecond test without threads:")
    # runs two sleep tests after each other
    await asyncio.gather(sleep_test_same_thread(), sleep_test_same_thread())

    print("\nThird test with tasks:")
    # runs two sleep tests after each other
    task1 = asyncio.create_task(sleep_test_same_thread())
    task2 = asyncio.create_task(sleep_test_same_thread())
    await asyncio.gather(task1, task2)

    print("\nForth test with tasks:")
    # runs two sleep tests in parallell and wait until both finish (same as asyncio.gather)
    task1 = asyncio.create_task(sleep_test_different_threads())
    task2 = asyncio.create_task(sleep_test_different_threads())
    await task1
    await task2

    print("\nFifth test without tasks:")
    # runs two sleep tests after each other (note that those are NOT executed in parallell)
    await sleep_test_different_threads()
    await sleep_test_different_threads()

asyncio.run(main())