import asyncio
from async_task import AsyncTask

class Task2(AsyncTask):

    async def run(self):
        print("Running Task2")
        while True:
            try:
                print('Task2 executing')
                await asyncio.sleep(1)
            except asyncio.CancelledError as e:
                print(f'Task2 received a request to cancel because of {e}, cleaning up task!!')
                break
        print("Task2 cleaned up and exiting")

    async def close(self, reason=""):
        print(f"Closing Task2, reason: {reason}")
        self.task.cancel(reason)