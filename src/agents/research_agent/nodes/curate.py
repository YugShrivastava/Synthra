from core.state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from rich.console import Console

def curate_node(state: AgentState):
    console = Console()
    """
    Uses Gemini llm to read the search data and write a polished report
    """
    with console.status(f"⚙️I am analyzing data and preparing report, Keep Up for Few Seconds!!",spinner="dots"):

        llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature = 0)

        prompt = f"""
        You are a professional research assistant. 
        Topic: {state['topic']}
        
        Here is the raw data gathered from the web:
        {state['search_data']}
        
        Please write a comprehensive, polished, and professional report on this topic.
        Structure it with clear headers. Do not use markdown symbols like ** or # in the final text 
        because we are printing this to a PDF. Just use plain text with clear spacing.
        """

        response = llm.invoke(prompt)
    return {"final_report": response.content}