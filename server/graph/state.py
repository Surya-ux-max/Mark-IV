from typing import Annotated, Sequence, TypedDict, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # LangGraph standard message adder
    messages: Annotated[Sequence[BaseMessage], add_messages]
    # Routing decision: the next node to execute
    next: str
    # Last node that was executed
    sender: str
    # Live execution trace log list for dashboard visualization
    trace: List[str]
    # Compiled response from the supervisor
    final_response: str
