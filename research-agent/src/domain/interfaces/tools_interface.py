from abc import ABC, abstractmethod
from typing import List, Dict, Any


class ToolsInterface(ABC):

    @abstractmethod
    async def decompose_tasks(self, user_query: str):
        pass

    @abstractmethod
    async def research_planner(self, sub_task_list: List[str]):
        pass

    @abstractmethod
    async def research_executor(self, research_topics: List[str]):
        pass

    @abstractmethod
    async def approach_comparator(self, research_topics: List[str], relevant_docs: List[Dict[str, Any]]):
        pass

    @abstractmethod
    async def solution_synthesizer(self, approaches: List[Dict[str, Any]]):
        pass

    @abstractmethod
    async def structured_plan_generator(self, selected_approach: Dict[str, Any]):
        pass
