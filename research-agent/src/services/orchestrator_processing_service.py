from typing import Optional, Dict, Any

from langchain_core.messages import HumanMessage
from loguru import logger

from agents.orchestrator_graph import OrchestratorGraph
from domain.interfaces.orchestrator_processing_interface import OrchestratorProcessingInterface
from domain.states.orchestrator_state import GraphState


def _create_initial_state(user_name: Optional[str], query: str):
    initial_state = GraphState(
        query=[HumanMessage(content=query)],
        response=None,
        tokens_used=None,
        user_name=user_name,
        state_metadata={},
        has_error=False,
        error_code="",
        error_severity="",
        error_context="",
        user_friendly_error="", )

    return initial_state

def _create_error_state(user_name: Optional[str], query: str, error_message: str):
    initial_state = GraphState(
        query=[HumanMessage(content=query)],
        response=f"Sorry, I encountered an error: {error_message}",
        tokens_used=None,
        user_name=user_name,
        state_metadata={
            "status": "error",
            "message": error_message,
        },
        has_error=True,
        error_code="UNABLE_TO_START_PROCESSING",
        error_severity="HIGH",
        error_context="",
        user_friendly_error="", )

    return initial_state


def graph_state_to_api_response(state: GraphState) -> Dict[str, Any]:
    metadata = state.get("state_metadata", {})

    return {
        "status": metadata.get("status", "completed"),
        "response": state.get("response", ""),
        "conversation_state": {
            "user_name": state.get("user_name"),
            "query": [msg.content if hasattr(msg, "content") else str(msg) for msg in state.get("query", [])],
            "tokens_used": state.get("tokens_used"),

            "has_error": state.get("has_error"),
            "error_code": state.get("error_code"),
            "error_severity": state.get("error_severity"),
            "user_friendly_error": state.get("user_friendly_error"),
        }
    }


class OrchestratorProcessingService(OrchestratorProcessingInterface):

    def __init__(self, orchestrator: OrchestratorGraph):
        self.orchestrator = orchestrator
        self.graph = self.orchestrator.graph.compile()


    async def process_user_query(self, user_name: str, query: str) -> GraphState:
        try:
            # Utilities.save_graph_as_jpg(self.graph, "../assets/orchestrator_graph.jpg")

            logger.info(f"Beginning graph execution for user {user_name}. Assigning initial state")
            initial_state = _create_initial_state(user_name, query)

            return await self._execute_graph(initial_state)

        except Exception as e:
            logger.error(f"Error starting new conversation: {e}")
            return _create_error_state(user_name, query, str(e))

    # -------------------
    # Helper Functions
    # -------------------

    async def _execute_graph(self, initial_state: GraphState) -> GraphState:
        try:
            logger.info("Executing orchestrator graph")

            final_state: GraphState = await self.graph.ainvoke(initial_state)

            if not final_state.get("response"):
                final_state["response"] = ""

            current_metadata = final_state.get("state_metadata", {})

            final_state["state_metadata"] = {
                **current_metadata,
                "status": "completed",
            }

            return final_state

        except Exception as e:
            logger.exception("LangGraph execution failed")
            return _create_error_state(initial_state["user_name"],
                                       initial_state["query"][-1].content,
                                       str(e))
