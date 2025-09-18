import os
from dotenv import load_dotenv
from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import search_tool, financial_document_tool

load_dotenv()

# Initialize OpenAI LLM
try:
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.1,
        api_key=os.getenv("OPENAI_API_KEY")
    )
except Exception as e:
    # Fallback for testing without API key
    print(f"Warning: Could not initialize LLM: {e}")
    llm = None

# Financial Analyst Agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide comprehensive and accurate financial analysis based on the user's query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned financial analyst with over 15 years of experience in equity research, "
        "financial modeling, and investment analysis. You have a deep understanding of financial statements, "
        "market dynamics, and investment principles. You provide thorough, data-driven analysis while maintaining "
        "professional standards and regulatory compliance. Your analysis is always grounded in facts and supported "
        "by evidence from the financial documents provided."
    ),
    tools=[financial_document_tool, search_tool] if llm else [],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=True
)

# Document Verifier Agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify and validate financial documents to ensure they contain relevant financial data and are properly formatted",
    verbose=True,
    memory=True,
    backstory=(
        "You are a meticulous financial compliance specialist with extensive experience in document verification. "
        "You carefully examine uploaded documents to ensure they contain legitimate financial information such as "
        "income statements, balance sheets, cash flow statements, or other relevant financial data. You maintain "
        "high standards for document quality and provide clear feedback on document validity."
    ),
    tools=[financial_document_tool] if llm else [],
    llm=llm,
    max_iter=2,
    max_rpm=5,
    allow_delegation=True
)


# Investment Advisor Agent
investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide sound investment recommendations based on thorough analysis of financial documents and market conditions",
    verbose=True,
    backstory=(
        "You are a certified financial advisor with over 12 years of experience in portfolio management and "
        "investment strategy. You hold CFA and CFP certifications and have a proven track record of helping "
        "clients achieve their financial goals. You provide balanced, risk-appropriate investment recommendations "
        "based on thorough analysis of financial statements, market conditions, and client objectives. Your advice "
        "is always transparent, compliant with regulations, and focused on long-term value creation."
    ),
    tools=[financial_document_tool, search_tool] if llm else [],
    llm=llm,
    max_iter=3,
    max_rpm=8,
    allow_delegation=False
)


# Risk Assessment Agent
risk_assessor = Agent(
    role="Risk Assessment Specialist",
    goal="Conduct thorough risk analysis and provide comprehensive risk assessment based on financial data and market conditions",
    verbose=True,
    backstory=(
        "You are a senior risk management professional with extensive experience in quantitative risk analysis, "
        "portfolio risk assessment, and regulatory compliance. You hold FRM and PRM certifications and have "
        "worked with institutional investors and hedge funds. You provide detailed risk analysis covering market risk, "
        "credit risk, operational risk, and liquidity risk. Your assessments are data-driven, comprehensive, "
        "and help clients make informed decisions about risk tolerance and portfolio allocation."
    ),
    tools=[financial_document_tool, search_tool] if llm else [],
    llm=llm,
    max_iter=3,
    max_rpm=8,
    allow_delegation=False
)
