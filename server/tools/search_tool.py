import os
import requests
from tools.browser_tool import search_duckduckgo

def search_tavily(query: str, max_results=4) -> str:
    """
    Executes web searches using Tavily Search API.
    If TAVILY_API_KEY is not set or query fails, falls back to DuckDuckGo scraper.
    """
    tavily_key = os.getenv("TAVILY_API_KEY", "")
    
    if not tavily_key:
        print("Tavily search key missing. Falling back to DuckDuckGo.")
        return search_duckduckgo(query)
        
    try:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": tavily_key,
            "query": query,
            "search_depth": "basic",
            "include_answer": False,
            "max_results": max_results
        }
        resp = requests.post(url, json=payload, timeout=8)
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            if results:
                summary_lines = []
                for idx, r in enumerate(results):
                    summary_lines.append(f"{idx+1}. [{r.get('title')}] ({r.get('url')}):\n   {r.get('content')}")
                return "\n\n".join(summary_lines)
            else:
                return "No search results found."
    except Exception as e:
        print(f"Tavily search failed: {e}. Falling back to DuckDuckGo.")
        
    return search_duckduckgo(query)
