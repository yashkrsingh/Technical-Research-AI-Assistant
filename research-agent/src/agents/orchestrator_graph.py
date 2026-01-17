from langchain_core.runnables.graph import Graph
from langgraph.graph import StateGraph

from agents.orchestrator_nodes import OrchestratorNodes
from domain.states.orchestrator_state import ResearchState


class OrchestratorGraph:

    def __init__(self, orchestrator_nodes: OrchestratorNodes):
        self.nodes = orchestrator_nodes
        self.graph = self._build_graph()


    def _build_graph(self) -> StateGraph:

        workflow = StateGraph(ResearchState)

        workflow.add_node(self.nodes.task_decomposer)
        workflow.add_node(self.nodes.research_planner)
        workflow.add_node(self.nodes.research_executor)
        workflow.add_node(self.nodes.approach_comparator)
        workflow.add_node(self.nodes.solution_synthesizer)


