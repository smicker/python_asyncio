import asyncio
from async_task import AsyncTask

class Task1(AsyncTask):

    async def run(self):
        print("Running Task1")
        while True:
            print('Task1 executing')
            await asyncio.sleep(1)

    def close(self, reason=""):
        print(f"Closing Task1, reason: {reason}")
        self.task.cancel()