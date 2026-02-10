from typing import Annotated
from src.agents.coding_agent.agent import coding_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from src.model.model import get_llm
from langgraph.prebuilt import create_react_agent
from src.agents.review_agent.tool import tools
from src.agents.review_agent.memory import ReviewState, checkpoint
from rich.console import Console
from src.agents.research_agent.core.graph import research_workflow


@tool
def delegate_to_coding_agent(
    task_description: Annotated[str, "Exact task that coding agent needs to do"], 
    project_id: Annotated[str, "Exact project_id to use for saving context as well as project directory name"]
):
    
    """
        This tool hands off coding tasks to the coding agent
        
        Args:
            task_description: str
            project_id: str
            
        returns a str 
    """
    
    prompt = f"""
        For project_id {project_id},
        {task_description}
    """
    
    config = {"configurable": {"thread_id": project_id}, "recursion_limit": 100}
    messages = [
        HumanMessage(content=prompt)
    ]
    
    
    for mode, chunk in coding_agent.stream(
        {"messages": messages},
        config=config,
        stream_mode=["messages", "updates"]
    ):
        if mode == "messages":
            message_chunk, metadata = chunk
            if hasattr(message_chunk, "content") and message_chunk.content:
                print(message_chunk.content, end="\n")
                
    print(coding_agent.get_state(project_id))

    return "✅ All Tasks Done!!"


@tool       
def interact(project_id: str, project_path: str, user_input: str) -> str:
    """Interact with the code review agent.
    
    Args:
        project_id: Unique identifier for the review session
        project_path: Absolute path to the codebase to review
        user_input: User's instruction/query
    
    Returns:
        str: Agent's response
    """
    llm = get_llm()
    
    agent = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=checkpoint,
        state_schema=ReviewState
    )
    
    config = {"configurable": {"thread_id": project_id}, "recursion_limit": 50}
    
    system_prompt = f"""You are an expert code review agent analyzing the codebase at: '{project_path}'

Your mission is to provide comprehensive, actionable code review feedback covering:

1. **Code Quality Analysis**
   - Review code style, readability, and maintainability
   - Identify code smells, anti-patterns, and potential bugs
   - Check for best practices adherence
   - Evaluate error handling and edge cases

2. **Project Structure & Architecture**
   - Analyze directory organization and file segregation
   - Identify architecture pattern (monolithic/modular/microservices)
   - Evaluate separation of concerns
   - Check for proper layering (presentation/business/data)

3. **Framework & Technology Stack**
   - Detect languages and frameworks used
   - Evaluate technology choices and their appropriateness
   - Check for deprecated dependencies or security vulnerabilities

4. **Git Repository Analysis** (if applicable)
   - Review commit history quality and patterns
   - Analyze contributor statistics
   - Evaluate commit message conventions
   - Check branch organization

5. **Code Metrics & Complexity**
   - Measure file sizes and code distribution
   - Identify overly complex files or functions
   - Check for code duplication

6. **Linting & Standards**
   - Run linters on code files
   - Report style violations and warnings

**IMPORTANT INSTRUCTIONS:**
- ALWAYS use the provided tools to gather information before making assessments
- Start by using 'list_project_files' to discover all files
- Use 'analyze_project_structure' for high-level architecture analysis
- Use 'git_analysis' if it's a git repository
- Sample key files using 'read_file' and 'get_file_metrics'
- Run 'lint_code_file' on important source files
- ALL tool calls must include project_id='{project_id}' as the first parameter
- Provide specific examples from the codebase in your feedback
- Be constructive: highlight both strengths and areas for improvement
- Organize your output in clear sections with markdown formatting
- Prioritize actionable recommendations

Current project_path: {project_path}
Current project_id: {project_id}
"""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"[Review Session: {project_id}] {user_input}")
    ]
    
    print("\n" + "="*80)
    print(f"🔍 CODE REVIEW AGENT INITIALIZED")
    print(f"📁 Project Path: {project_path}")
    print(f"🆔 Session ID: {project_id}")
    print("="*80 + "\n")
    
    try:
        for mode, chunk in agent.stream(
            {"messages": messages},
            config=config,
            stream_mode=["messages", "updates"]
        ):
            if mode == "messages":
                message_chunk, metadata = chunk
                if hasattr(message_chunk, "content") and message_chunk.content:
                    print(message_chunk.content, end="", flush=True)
        
        print("\n\n" + "="*80)
        print("✅ CODE REVIEW COMPLETED")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n\n❌ ERROR during review: {str(e)}\n")
        return f"ERROR: {str(e)}"
    
    return "✅ Review session completed successfully"



@tool
def delegate_to_research_agent(topic:str)->str:
    """
    This tool hands off coding tasks to the coding agent
        
        Args:
            topic: Research topic for research agent

    returns a str

    """

    app = research_workflow()
    console = Console()
    console.clear()
    console.print(r"""
            _____
        _/ ____\_
        /  ( -- )  \
        |  /  oo  \  |
        \_\  __  /_/
            |      |
        __|  __  |__
        /  \      /  \
        
        [ Research AGENT]
        """)
    console.print("Hey, I am your ResearchAgent..")
    inputs = {"topic": topic}

    app.invoke(inputs)
    return "✅All Tasks Done"
