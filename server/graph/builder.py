from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver

# Import state schema and node bindings
from graph.state import AgentState
from graph.nodes import (
    supervisor_node,
    github_node,
    weather_node,
    browser_node,
    coding_node,
    memory_node,
    browser_cleaner_node,
    calendar_node,
    email_node
)
from graph.router import route_next_node

def build_survex_graph():
    # Initialize the state graph
    workflow = StateGraph(AgentState)
    
    # 1. Define nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("github_agent", github_node)
    workflow.add_node("weather_agent", weather_node)
    workflow.add_node("browser_agent", browser_node)
    workflow.add_node("coding_agent", coding_node)
    workflow.add_node("memory_agent", memory_node)
    workflow.add_node("browser_cleaner", browser_cleaner_node)
    workflow.add_node("calendar_agent", calendar_node)
    workflow.add_node("email_agent", email_node)
    
    # 2. Add entry points
    workflow.add_edge(START, "supervisor")
    
    # 3. Add edges from specialized agents back to supervisor
    workflow.add_edge("github_agent", "supervisor")
    workflow.add_edge("weather_agent", "supervisor")
    workflow.add_edge("browser_agent", "supervisor")
    workflow.add_edge("coding_agent", "supervisor")
    workflow.add_edge("memory_agent", "supervisor")
    workflow.add_edge("browser_cleaner", "supervisor")
    workflow.add_edge("calendar_agent", "supervisor")
    workflow.add_edge("email_agent", "supervisor")
    
    # 4. Add conditional edges from supervisor to agents or termination
    workflow.add_conditional_edges(
        "supervisor",
        route_next_node,
        {
            "github_agent": "github_agent",
            "weather_agent": "weather_agent",
            "browser_agent": "browser_agent",
            "coding_agent": "coding_agent",
            "memory_agent": "memory_agent",
            "browser_cleaner": "browser_cleaner",
            "calendar_agent": "calendar_agent",
            "email_agent": "email_agent",
            "__end__": "__end__"
        }
    )
    
    # Compile workflow with session checkpointer saver
    memory_saver = MemorySaver()
    compiled_graph = workflow.compile(checkpointer=memory_saver)
    return compiled_graph
