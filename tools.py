import os
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader
from langchain.tools import tool

load_dotenv()

# Search tool for web research
search_tool = SerperDevTool()

# PDF document reader tool
@tool
def financial_document_tool(path: str = 'data/sample.pdf') -> str:
    """Tool to read and extract text from financial PDF documents

    Args:
        path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

    Returns:
        str: Full Financial Document file
    """
    try:
        loader = PyPDFLoader(path)
        docs = loader.load()

        full_report = ""
        for data in docs:
            # Clean and format the financial document data
            content = data.page_content
            
            # Remove extra whitespaces and format properly
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
                
            full_report += content + "\n"
            
        return full_report
    except Exception as e:
        return f"Error reading PDF file: {str(e)}"

# Additional analysis tools can be added here as needed