from domain.interfaces.tools_interface import ToolsInterface
from domain.states.orchestrator_state import ResearchState


class OrchestratorNodes:

    def __init__(self, tools_service: ToolsInterface):
        self.tools_service = tools_service

    async def task_decomposer(self, state: ResearchState):
        """ Converts vague goals into a set of defined technical asks """
        pass

    async def research_planner(self, state: ResearchState):
        """ Decides what needs research and what can be output directly """
        pass

    async def research_executor(self, state: ResearchState):
        """ Researches the top needed tech asks via RAG """
        pass

    async def approach_comparator(self, state: ResearchState):
        """ Compares the various technical approaches that are valid for the query """
        pass

    async def solution_synthesizer(self, state: ResearchState):
        """ Picks the final approach that is most suitable for the query """
        pass

    async def plan_generator(self, state: ResearchState):
        """ Generates the final plan for the query """
        pass
