from graph.state import AgentState

def route_next_node(state: AgentState):
    """
    Evaluates the state['next'] field set by the supervisor 
    to decide which node LangGraph should execute next.
    """
    next_node = state.get("next", "__end__")
    # Return '__end__' or the target agent name
    return next_node
