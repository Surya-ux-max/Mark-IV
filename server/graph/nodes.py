from langchain_core.messages import AIMessage
from graph.state import AgentState

# Import specialized agents
from agents.supervisor import run_supervisor, compile_final_response
from agents.github_agent import run_github_agent
from agents.weather_agent import run_weather_agent
from agents.browser_agent import run_browser_agent
from agents.coding_agent import run_coding_agent
from agents.memory_agent import run_memory_agent

def supervisor_node(state: AgentState):
    # Determine the next node to route to
    next_node = run_supervisor(state["messages"], state["trace"])
    
    # Update state properties
    state_update = {
        "next": next_node,
        "sender": "supervisor"
    }
    
    # If terminating, compile the final conversational reply
    if next_node == "__end__":
        final_reply = compile_final_response(state["messages"])
        state_update["final_response"] = final_reply
        
    return state_update

def github_node(state: AgentState):
    output = run_github_agent(state["messages"])
    # Append AIMessage result and record trace steps
    return {
        "messages": [AIMessage(content=output, name="github_agent")],
        "sender": "github_agent",
        "trace": state["trace"] + ["github_agent"]
    }

def weather_node(state: AgentState):
    output = run_weather_agent(state["messages"])
    return {
        "messages": [AIMessage(content=output, name="weather_agent")],
        "sender": "weather_agent",
        "trace": state["trace"] + ["weather_agent"]
    }

def browser_node(state: AgentState):
    output = run_browser_agent(state["messages"])
    return {
        "messages": [AIMessage(content=output, name="browser_agent")],
        "sender": "browser_agent",
        "trace": state["trace"] + ["browser_agent"]
    }

def coding_node(state: AgentState):
    output = run_coding_agent(state["messages"])
    return {
        "messages": [AIMessage(content=output, name="coding_agent")],
        "sender": "coding_agent",
        "trace": state["trace"] + ["coding_agent"]
    }

def memory_node(state: AgentState):
    output = run_memory_agent(state["messages"])
    return {
        "messages": [AIMessage(content=output, name="memory_agent")],
        "sender": "memory_agent",
        "trace": state["trace"] + ["memory_agent"]
    }

# Import Browser Cache Cleaner tool agent
from agents.browser_cleaner import run_browser_cache_cleaner

def browser_cleaner_node(state: AgentState):
    output = run_browser_cache_cleaner()
    return {
        "messages": [AIMessage(content=output, name="browser_cleaner")],
        "sender": "browser_cleaner",
        "trace": state["trace"] + ["browser_cleaner"]
    }

# Import Calendar and Email Agents
from agents.calendar_agent import run_calendar_agent
from agents.email_agent import run_email_agent

def calendar_node(state: AgentState):
    output = run_calendar_agent(state["messages"])
    return {
        "messages": [AIMessage(content=output, name="calendar_agent")],
        "sender": "calendar_agent",
        "trace": state["trace"] + ["calendar_agent"]
    }

def email_node(state: AgentState):
    output = run_email_agent(state["messages"])
    return {
        "messages": [AIMessage(content=output, name="email_agent")],
        "sender": "email_agent",
        "trace": state["trace"] + ["email_agent"]
    }
