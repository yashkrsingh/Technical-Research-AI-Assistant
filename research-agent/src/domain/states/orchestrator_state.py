from typing import TypedDict, List, Annotated, Optional, Any, Dict

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages


class GraphState(TypedDict):
    query: Annotated[List[AnyMessage], add_messages]
    response: Optional[str]
    tokens_used: Optional[List[str]]
    user_name: Optional[str]

    state_metadata: Optional[Dict[str, Any]]

    has_error: Optional[bool]
    error_code: Optional[str]
    error_severity: Optional[str]
    error_context: Optional[str]
    user_friendly_error: Optional[str]
