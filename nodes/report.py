from fpdf import FPDF
from core.state import AgentState
import os
from rich.text import Text
from rich.console import Console
from rich.panel import Panel

def pdf_node(state:AgentState) -> None:
    """
    Takes the final report and save it as a PDF.
    """

    print("Generating PDF....")

    console = Console()
    with console.status("[bold magenta]Compiling PDF document...[/bold magenta]", spinner="dots"):    
        report_text = state['final_report']
        os.makedirs("reports", exist_ok=True)
        filename = f"reports/{state['topic'].replace(' ', '_')}_Report.pdf"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        #Add Title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt= f"Research Report: {state['topic']}", ln=1, align='C')


        #Body
        pdf.set_font("Arial", size=12)
        # multi_cell to handle text wrapping automatically
        # encode/decode to strip non-latin characters avoiding basic FPDF crash
        safe_text = report_text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, txt=safe_text)
        
        pdf.output(filename)
    success_text = Text()
    success_text.append(f"Topic: {state['topic']}\n", style="bold white")
    success_text.append(f"File: {filename}\n", style="underline blue")
    success_text.append("Status: Complete", style="bold green")
    console.print(Panel(success_text, title="Research Agent Finished", border_style="green"))
    print(f"Success! PDF Saved: {filename}")
    return


