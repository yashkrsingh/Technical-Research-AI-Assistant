from abc import ABC, abstractmethod

from domain.states.orchestrator_state import GraphState


class OrchestratorProcessingInterface(ABC):

    @abstractmethod
    async def process_user_query(self, user_name: str, query: str) -> GraphState:
        pass