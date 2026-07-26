import time
from database.db import log_agent_execution, log_supervisor_decision

class ObservabilityTracker:
    # Memory tracker dictionary
    _active_runs = {}

    @staticmethod
    def start_execution(session_id: str, agent_id: str):
        """Starts timing an agent execution run."""
        run_key = f"{session_id}_{agent_id}"
        ObservabilityTracker._active_runs[run_key] = time.time()
        print(f"Observability: Started execution for {agent_id} in session {session_id}")

    @staticmethod
    def end_execution(session_id: str, agent_id: str, logs: str, status="SUCCESS", tools_list=None):
        """Calculates runtime latency and logs execution metrics to database."""
        if tools_list is None:
            tools_list = []
            
        run_key = f"{session_id}_{agent_id}"
        start_time = ObservabilityTracker._active_runs.pop(run_key, None)
        
        if start_time:
            runtime = time.time() - start_time
        else:
            runtime = 0.0
            
        print(f"Observability: Completed execution for {agent_id} in {runtime:.3f}s. Status: {status}")
        
        try:
            log_agent_execution(session_id, agent_id, logs, runtime, status, tools_list)
        except Exception as e:
            print(f"Observability: Database logging failed for agent execution: {e}")

    @staticmethod
    def track_supervisor_routing(session_id: str, intent: str, selected_agents: list, reasoning: str, token_usage: int):
        """Tracks the decision trajectory and token usage of the supervisor agent."""
        print(f"Observability: Supervisor routed to {selected_agents} (tokens: {token_usage})")
        try:
            log_supervisor_decision(session_id, intent, selected_agents, reasoning, token_usage)
        except Exception as e:
            print(f"Observability: Database logging failed for supervisor decision: {e}")
