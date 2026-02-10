from langgraph.graph import StateGraph,END
from langgraph.graph.state import CompiledStateGraph
from core.state import AgentState
from nodes.curate import curate_node
from nodes.report import pdf_node
from nodes.research import research_node

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
