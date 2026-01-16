from abc import ABC, abstractmethod


class ToolsInterface(ABC):

    @abstractmethod
    async def get_task_list(self):
        pass