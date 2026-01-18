from langgraph.graph import StateGraph

from agents.orchestrator_nodes import OrchestratorNodes
from domain.states.orchestrator_state import ResearchState


class OrchestratorGraph:

    def __init__(self, orchestrator_nodes: OrchestratorNodes):
        self.nodes = orchestrator_nodes
        self.graph = self._build_graph()


    def _build_graph(self) -> StateGraph:

        workflow = StateGraph(ResearchState)

        workflow.add_node("decompose", self.nodes.task_decomposer)
        workflow.add_node("planner", self.nodes.research_planner)
        workflow.add_node("executor", self.nodes.research_executor)
        workflow.add_node("comparator", self.nodes.approach_comparator)
        workflow.add_node("synthesizer", self.nodes.solution_synthesizer)
        workflow.add_node("generator", self.nodes.plan_generator)

        workflow.set_entry_point("decompose")

        workflow.add_edge("decompose", "planner")
        workflow.add_edge("planner", "executor")
        workflow.add_edge("executor", "comparator")
        workflow.add_edge("comparator", "synthesizer")
        workflow.add_edge("synthesizer", "generator")

        return workflow


