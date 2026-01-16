from domain.states.orchestrator_state import GraphState


class OrchestratorNodes:

    def __init__(self):
        pass

    async def task_decomposer(self, state: GraphState):
        """ Converts vague goals into a set of defined technical asks """
        pass

    async def research_planner(self, state: GraphState):
        """ Decides what needs research and what can be output directly """
        pass

    async def research_executor(self, state: GraphState):
        """ Researches the top needed tech asks via RAG """
        pass

    async def approach_comparator(self, state: GraphState):
        """ Compares the various technical approaches that are valid for the query """
        pass

    async def solution_synthesizer(self, state: GraphState):
        """ Picks the final approach that is most suitable for the query """
        pass
