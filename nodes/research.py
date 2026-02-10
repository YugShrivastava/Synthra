from langchain_tavily import TavilySearch
from core.state import AgentState
from rich.console import Console
import time

def research_node(state: AgentState):
    """
    Takes the topic, searches the web, gathers raw data.
    """
    console = Console()
    #initalize tavily ssearch
    with console.status(f"[bold cyan]Searching the web for: {state['topic']}...[/bold cyan]", spinner="earth"):
        tool = TavilySearch(max_results=5)
        search_results = tool.invoke(state['topic'])

        time.sleep(1)
        #format results into a string
        raw_content = "\n".join([res['content'] for res in search_results['results']])
    console.print(f" [green]Found {len(search_results['results'])} relevant sources.[/green]")
    return {"search_data": raw_content}