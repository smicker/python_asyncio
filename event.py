"""
This demo shows how you can use asyncio.Event to handle execution control. Since the signal control
is not injected to asyncio, but instead handled by signal.signal(), it will not be noticed by asyncio.
Therefor we need to use the call_soon_threadsafe() method to notify asyncio of the QUIT.set().
A better approach is to inject the signal control to asyncio to get rid of this problem, see demo
"event_with_asyncio_signal_handler.py".

Printout:
    Main starts
    Main waiting for QUIT
    Executing my_task
    Executing my_task
    Executing my_task
    ^CCtrl+c pressed
    Main returned
    Exiting main
    Ending my_task
"""

import asyncio
import contextlib
import signal

QUIT: asyncio.Event = asyncio.Event()

def sig_handler(signum, _frame):
    """Signal handler"""
    print("Ctrl+c pressed")

    # If you call QUIT.set() directly here the asyncio event loop will not notice
    # it. This is because this signal interrupt, even though it executes in the
    # same thread as the rest of the code here, is not handled by the asyncio event
    # loop. So it will not wake up the event loop "select". To fix this, you should
    # instead put the QUIT.set() as a task through call_soon_threadsafe.
    #QUIT.set()  # QUIT.wait() does not return directly when this is called!!

    # Solution, use call_soon_threadsafe since it will wake up the asyncio event
    # loop "select" which will make the event loop aware of that QUIT is set.
    # Notice that using call_soon(QUIT.set) is not enough since that will not trigger
    # the event loop "select".
    asyncio.get_running_loop().call_soon_threadsafe(QUIT.set)

async def event_wait(evt: asyncio.Event, timeout: int):
    """This is a helper function to simulate threading.Event.wait(). It will not throw any
    TimeoutError if timing out. It will just return False if timing out or True if
    event is set."""
    # Suppress TimeoutError because we'll return False in case of timeout
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(evt.wait(), timeout)
    return evt.is_set()

async def my_task():
    while not QUIT.is_set():
        print("Executing my_task")
        await event_wait(QUIT, 1)
    print("Ending my_task")

async def task_quitter():
    print("Tester start")
    await asyncio.sleep(2)
    QUIT.set()  # QUIT.wait() is noticed by asyncio directly if this is called
    print("Tester quit")

async def main():
    print("Main starts")

    # setup signal handler
    signal.signal(signal.SIGINT, sig_handler)  # Keyboard: Ctrl-C
    signal.signal(signal.SIGTERM, sig_handler)  # Unix only

    task = asyncio.create_task(my_task())

    # Test to quit from a task
    #task = asyncio.create_task(task_quitter())

    try:
        print("Main waiting for QUIT")
        # You can use the wait_for directly without using my helper function "event_wait", as below,
        # but then you'll have to catch an eventually asyncio.TimeoutError.
        await asyncio.wait_for(QUIT.wait(), 10)
        print("Main returned")
    except asyncio.TimeoutError:
        print("Timed out")

    print("Exiting main")

asyncio.run(main())