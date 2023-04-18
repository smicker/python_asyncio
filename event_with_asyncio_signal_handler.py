"""
This demo shows how you can use asyncio.Event to handle execution control. It adds the signal control
to the asyncio. The difference between this and the event.py demo is that by adding the signal control
to the asyncio, you don't need to use the call_soon_threadsafe() method since it will automatically be
controlled by asyncio loop. So this is a little bit cleaner.

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

def signal_handler():
    """Signal handler"""
    print("Ctrl+c pressed")
    QUIT.set()

async def event_wait(event: asyncio.Event, timeout: int):
    """This is a helper function to simulate threading.Event.wait(). It will not throw any
    TimeoutError if timing out. It will just return False if timing out or True if
    event is set."""
    # Suppress TimeoutError because we'll return False in case of timeout
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(event.wait(), timeout)
    return event.is_set()

async def my_task():
    while not QUIT.is_set():
        print("Executing my_task")
        await event_wait(QUIT, 1)
    print("Ending my_task")

async def main():
    print("Main starts")

    # setup signal handler and inject it to asyncio
    for sig in ('SIGINT', 'SIGTERM'):
        asyncio.get_running_loop().add_signal_handler(getattr(signal, sig), signal_handler)

    task = asyncio.create_task(my_task())

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