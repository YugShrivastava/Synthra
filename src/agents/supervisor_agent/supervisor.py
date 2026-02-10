from src.model.model import llm
from src.agents.supervisor_agent.tool import delegate_to_coding_agent, interact, delegate_to_research_agent
from langchain_core.messages import HumanMessage
from src.agents.coding_agent.agent import coding_agent
from langgraph_supervisor import create_supervisor
from langgraph.errors import GraphRecursionError

supervisor_agent = create_supervisor(
    [coding_agent],
    model=llm,
    tools=[
        delegate_to_coding_agent,
        interact, 
        delegate_to_research_agent
    ]

)

supervisor_agent = supervisor_agent.compile()

def create_orchestrator_with_agents(user_prompt):        
    # user_prompt = input("Hey! What do you want me to do? : ")

    try:
        supervisor_agent.invoke({"messages": [HumanMessage(user_prompt)]}, config={"recursion_limit": 100})
    except GraphRecursionError as e:
        print("All tasks done")