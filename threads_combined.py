"""
This demo mixes an asyncio call with a callback and code running in another thread.
Exit with ctrl+c

Printout:
    step1 finished
    step2 started
    Here
    Activity forever
    Activity forever
    step2 finished
    Result from step2: hej
    Activity forever
    Activity forever
    Activity forever
    ^CCtrl+c pressed
    Exiting
"""

import asyncio
import time

async def step1():
    while True:
        await asyncio.sleep(1.0)
        # job = await inputQueue1.get()
        # good, we have handled that first task; we're done
        break
    print("step1 finished")

def step2():
    print("step2 started")
    # note: this is sync, not async, but it's executed in an own thread
    time.sleep(3)
    print("step2 finished")
    return "hej"

async def activity_forever():
    # this is the async queue loop
    while True:
        await asyncio.sleep(1.0)
        # job = await inputQueue1.get()
        # do something with this incoming job
        print("Activity forever")

def callback_from_step2(result):
    print(f"Result from step2: {result.result()}")

class Activities:
    def __init__(self, loop):
        self.loop = loop
        self.task1: asyncio.Task | None = None
        self.task2: asyncio.Task | None = None

    def run(self):
        self.task1 = self.loop.create_task(step1())
        self.task1.add_done_callback(self.run2)

    def run2(self, fut):
        try:
            if fut.exception() is not None:  # do nothing if task1 failed
                return
        except asyncio.CancelledError:  # or if it was cancelled
            return

        # Now run the sync step 2 in a thread (None means the default thread).
        # This will not block!!
        a = self.loop.run_in_executor(None, step2)
        a.add_done_callback(callback_from_step2)

        print(f"Here")

        # finally, run activity_forever as a task
        self.task2 = self.loop.create_task(activity_forever())

    async def cancel_gracefully(self):
        if self.task2 is not None:
            # in this case, task1 has already finished without error
            self.task2.cancel()
            try:
                await self.task2
            except asyncio.CancelledError:
                pass
        elif self.task1 is not None:
            self.task1.cancel()
            try:
                await self.task1
            except asyncio.CancelledError:
                pass

def mainprogram():
    # I don't know how to rewrite this in a modern way so I have to
    # use loop here bacause lack of understanding.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    acts = Activities(loop)
    loop.call_soon(acts.run)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Ctrl+c pressed")
    loop.run_until_complete(acts.cancel_gracefully())
    print("Exiting")

if __name__ == "__main__":
    mainprogram()