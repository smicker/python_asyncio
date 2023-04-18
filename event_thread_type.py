"""
This is an example showing that the threading.Event cannot be used together with asyncio. This
is because the threaading.Event will block and not giving back the control to asyncio loop.
This program will block inside the while loop in the mainloop.

Printout:
    Worker 1 started.
    Worker 2 started.
    Start mainloop
"""

import asyncio
import signal
import threading

THREAD_QUIT: threading.Event = threading.Event()  # Flag to tell whole app to quit

def sig_handler(signum, _frame):
    """Signal handler"""
    THREAD_QUIT.set()
    print(f"[app] sig_handler: got signal ctrl+c - terminating!")

async def worker(n):
    print(f"Worker {n} started.")
    await asyncio.sleep(2)
    print(f"Worker {n} ended.")

async def mainloop():
    print("Start mainloop")
    while not THREAD_QUIT.is_set():
        THREAD_QUIT.wait(timeout=30)
        await asyncio.sleep(0)
    print("Exit mainloop")

async def main():
    # setup signal handler
    signal.signal(signal.SIGINT, sig_handler)  # Keyboard: Ctrl-C
    signal.signal(signal.SIGTERM, sig_handler)  # Keyboard: Ctrl-C

    workers = []
    workers.append(asyncio.create_task(worker(1)))
    workers.append(asyncio.create_task(worker(2)))

    ml = asyncio.create_task(mainloop())
    await asyncio.gather(ml)
    for task in workers:
        task.cancel()


if __name__ == '__main__':
    asyncio.run(main())
    print("Exit program")