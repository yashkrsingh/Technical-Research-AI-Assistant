from typing import TypedDict, List, Annotated, Optional, Any, Dict

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages


class ResearchState(TypedDict):
    query: Annotated[List[AnyMessage], add_messages]
    response: Optional[str]
    tokens_used: Optional[List[str]]
    user_name: Optional[str]

    subtasks: Optional[List[str]]
    research_queries: Optional[List[str]]
    relevant_docs: Optional[List[Dict[str, Any]]]
    citations: Optional[List[str]]
    approaches: Optional[List[Dict[str, Any]]]
    recommended_approach: Optional[Dict[str, Any]]
    reasoning: Optional[str]
    final_plan: Optional[Dict[str, Any]]

    state_metadata: Optional[Dict[str, Any]]

    has_error: Optional[bool]
    error_code: Optional[str]
    error_severity: Optional[str]
    error_context: Optional[str]
    user_friendly_error: Optional[str]

