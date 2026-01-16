from fastapi import APIRouter

from api.dependency_injection import OrchestratorProcessingServiceDependency
from services.orchestrator_processing_service import graph_state_to_api_response

agent_api_router = APIRouter()

@agent_api_router.get("/call-agent", tags=["Agent"])
async def answer_technical_questions(user_name: str, query: str,
                                     orchestrator_processing_service: OrchestratorProcessingServiceDependency):
    graph_state = await orchestrator_processing_service.process_user_query(user_name, query)
    api_response = graph_state_to_api_response(graph_state)
    return api_response
