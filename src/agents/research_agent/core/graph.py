from langgraph.graph import StateGraph,END
from langgraph.graph.state import CompiledStateGraph
from src.agents.research_agent.core.state import AgentState
from src.agents.research_agent.nodes.curate import curate_node
from src.agents.research_agent.nodes.report import pdf_node
from src.agents.research_agent.nodes.research import research_node

def research_workflow() -> CompiledStateGraph:
    workflow = StateGraph(AgentState)

    #add nodes

    workflow.add_node("researcher",research_node)
    workflow.add_node("writer", curate_node)
    workflow.add_node("publisher", pdf_node)

    #Add edges
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "publisher")

    #final step
    workflow.add_edge("publisher", END)

    return workflow.compile()
