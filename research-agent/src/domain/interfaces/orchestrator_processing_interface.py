from abc import ABC, abstractmethod

from domain.states.orchestrator_state import ResearchState


class OrchestratorProcessingInterface(ABC):

    @abstractmethod
    async def process_user_query(self, user_name: str, query: str) -> ResearchState:
        pass