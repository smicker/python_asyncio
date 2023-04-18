from abc import ABC, abstractmethod

class AsyncTask(ABC):

    def set_task(self, task):
        self.task = task

    def get_task(self):
        return self.task

    @abstractmethod
    async def run(self):
        pass

    @abstractmethod
    async def close(self):
        pass