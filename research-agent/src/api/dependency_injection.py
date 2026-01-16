from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from agents.orchestrator_graph import OrchestratorGraph
from agents.orchestrator_nodes import OrchestratorNodes
from domain.interfaces.orchestrator_processing_interface import OrchestratorProcessingInterface
from domain.interfaces.tools_interface import ToolsInterface
from services.orchestrator_processing_service import OrchestratorProcessingService
from services.tools_service import ToolsService


class Dependencies:

    @staticmethod
    @lru_cache()
    def get_tools_service():
        return ToolsService()

    @staticmethod
    @lru_cache()
    def orchestrator_nodes(tools_service: ToolsInterface = Depends(get_tools_service)) -> OrchestratorNodes:
        return OrchestratorNodes(tools_service=tools_service)

    @staticmethod
    @lru_cache()
    def orchestrator_graph(
            orchestrator_nodes: OrchestratorNodes = Depends(orchestrator_nodes)) -> OrchestratorGraph:
        return OrchestratorGraph(orchestrator_nodes=orchestrator_nodes)

    @staticmethod
    def orchestrator_processing_service(orchestrator_graph: OrchestratorGraph = Depends(orchestrator_graph)) -> OrchestratorProcessingInterface:
        return OrchestratorProcessingService(orchestrator=orchestrator_graph)

OrchestratorProcessingServiceDependency = Annotated[OrchestratorProcessingInterface, Depends(Dependencies.orchestrator_processing_service)]
