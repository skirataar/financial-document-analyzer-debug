from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, financial_document_tool

# Main financial document analysis task
analyze_financial_document = Task(
    description="""Analyze the financial document provided and address the user's query: {query}
    
    Your analysis should include:
    1. Document Overview: Summary of the financial document type and key information
    2. Financial Metrics: Extract and analyze key financial ratios, revenue, profit, debt, etc.
    3. Market Context: Research current market conditions and industry trends
    4. Investment Analysis: Provide investment insights based on the financial data
    5. Risk Assessment: Identify potential risks and opportunities
    6. Recommendations: Provide actionable investment recommendations
    
    Use the financial document tool to read the PDF and search tool for market research.""",

    expected_output="""Provide a comprehensive financial analysis report with the following structure:
    
    ## Executive Summary
    - Brief overview of findings and key recommendations
    
    ## Financial Analysis
    - Key financial metrics and ratios
    - Revenue, profit, and growth analysis
    - Balance sheet and cash flow insights
    
    ## Market Analysis
    - Industry trends and market conditions
    - Competitive positioning
    - Market opportunities and threats
    
    ## Investment Recommendations
    - Buy/Hold/Sell recommendation with rationale
    - Target price or valuation range
    - Risk factors to consider
    
    ## Risk Assessment
    - Key risks identified
    - Risk mitigation strategies
    - Portfolio allocation suggestions""",

    agent=financial_analyst,
    tools=[],  # Tools will be added at runtime
    async_execution=False,
)

# Investment analysis task
investment_analysis = Task(
    description="""Provide detailed investment analysis based on the financial document and user query: {query}
    
    Focus on:
    1. Valuation Analysis: Calculate key valuation metrics (P/E, P/B, EV/EBITDA, etc.)
    2. Financial Health: Assess profitability, liquidity, and solvency ratios
    3. Growth Prospects: Analyze revenue and earnings growth trends
    4. Competitive Position: Evaluate market position and competitive advantages
    5. Investment Thesis: Develop clear buy/hold/sell recommendation with supporting evidence""",

    expected_output="""Provide a structured investment analysis report:
    
    ## Valuation Summary
    - Key valuation metrics and comparisons to industry peers
    - Fair value estimate and target price range
    
    ## Financial Health Assessment
    - Profitability analysis (ROE, ROA, margins)
    - Liquidity and solvency ratios
    - Debt analysis and creditworthiness
    
    ## Growth Analysis
    - Revenue and earnings growth trends
    - Future growth prospects and drivers
    - Market expansion opportunities
    
    ## Investment Recommendation
    - Clear buy/hold/sell recommendation
    - Risk-adjusted return expectations
    - Time horizon and key catalysts""",

    agent=investment_advisor,
    tools=[],
    async_execution=False,
)

# Risk assessment task
risk_assessment = Task(
    description="""Conduct comprehensive risk assessment based on the financial document and user query: {query}
    
    Analyze the following risk categories:
    1. Market Risk: Exposure to market volatility and economic cycles
    2. Credit Risk: Default risk and creditworthiness assessment
    3. Operational Risk: Business operations and management risks
    4. Liquidity Risk: Cash flow and funding risks
    5. Regulatory Risk: Compliance and regulatory environment risks
    6. Concentration Risk: Portfolio concentration and diversification needs""",

    expected_output="""Provide a detailed risk assessment report:
    
    ## Risk Summary
    - Overall risk rating and key risk factors
    - Risk tolerance assessment and recommendations
    
    ## Market Risk Analysis
    - Beta analysis and market sensitivity
    - Economic cycle exposure
    - Interest rate and inflation risks
    
    ## Credit Risk Assessment
    - Credit quality and default probability
    - Debt structure and repayment capacity
    - Credit rating implications
    
    ## Operational Risk Review
    - Management quality and governance
    - Business model sustainability
    - Operational efficiency metrics
    
    ## Risk Mitigation Strategies
    - Diversification recommendations
    - Hedging strategies
    - Risk monitoring guidelines""",

    agent=risk_assessor,
    tools=[],
    async_execution=False,
)

    
# Document verification task
verification = Task(
    description="""Verify and validate the uploaded document to ensure it contains relevant financial information.
    
    Check for:
    1. Document Type: Confirm it's a financial document (10-K, 10-Q, annual report, etc.)
    2. Content Quality: Ensure readable financial data and statements
    3. Completeness: Verify key financial sections are present
    4. Format: Check if PDF is properly formatted and readable
    5. Relevance: Confirm document is suitable for financial analysis""",

    expected_output="""Provide a document verification report:
    
    ## Document Validation
    - Document type and format confirmation
    - Content quality assessment
    - Readability and completeness check
    
    ## Financial Content Analysis
    - Key financial sections identified
    - Data quality and accuracy assessment
    - Missing or incomplete sections noted
    
    ## Recommendations
    - Document suitability for analysis
    - Any issues or limitations identified
    - Suggestions for improved analysis""",

    agent=verifier,
    tools=[],
    async_execution=False
)