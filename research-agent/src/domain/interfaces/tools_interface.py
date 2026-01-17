from abc import ABC, abstractmethod
from typing import List


class ToolsInterface(ABC):

    @abstractmethod
    async def decompose_tasks(self, user_query: str):
        pass

    @abstractmethod
    async def research_planner(self, sub_task_list: List[str]):
        pass

    @abstractmethod
    async def approach_comparator(self, sub_task_list: List[str], relevant_docs: List[str]):
        pass

    @abstractmethod
    async def solution_synthesizer(self, sub_task_list: List[str]):
        pass

