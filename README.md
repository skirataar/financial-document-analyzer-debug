# Financial Document Analyzer

A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents.

## Features

- **PDF Document Processing**: Upload and analyze financial PDF documents
- **AI-Powered Analysis**: Multi-agent system with specialized financial analysts
- **Investment Recommendations**: Detailed investment analysis and recommendations
- **Risk Assessment**: Comprehensive risk analysis and mitigation strategies
- **Queue Processing**: Background task processing for concurrent requests
- **Database Storage**: Persistent storage of analysis results and metrics
- **REST API**: Complete API with status tracking and result retrieval

## Architecture

The system uses a multi-agent approach with specialized AI agents:
- **Financial Analyst**: Core financial analysis and document processing
- **Investment Advisor**: Investment recommendations and portfolio analysis
- **Risk Assessor**: Risk evaluation and mitigation strategies
- **Document Verifier**: Document validation and quality assurance

## Setup

### Prerequisites
- Python 3.8+
- Redis server
- OpenAI API key
- Serper API key (for web search)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create environment file:
```bash
cp .env.example .env
# Add your API keys to .env
```

3. Start Redis server:
```bash
redis-server
```

4. Start Celery worker:
```bash
celery -A queue_worker worker --loglevel=info
```

5. Start the application:
```bash
python run.py
```

Or manually:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Usage

### Analyze Document
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@financial_report.pdf" \
  -F "query=Analyze this quarterly report for investment opportunities"
```

### Check Task Status
```bash
curl "http://localhost:8000/task/{task_id}"
```

### Get Results
```bash
curl "http://localhost:8000/task/{task_id}/result"
```

## API Endpoints

- `POST /analyze` - Upload and analyze financial documents
- `GET /task/{task_id}` - Check task status
- `GET /task/{task_id}/result` - Get analysis results
- `GET /results` - Get paginated analysis history
- `GET /health` - Health check

## Bug Fixes and Improvements

### Deterministic Bugs Fixed

1. **Circular Reference Bug** - Fixed `llm = llm` in agents.py
2. **Missing Import Bug** - Fixed `Pdf` class import in tools.py
3. **Async Method Bug** - Fixed incorrect async method definition
4. **Kickoff Parameters Bug** - Fixed CrewAI kickoff input format
5. **Function Name Collision** - Renamed conflicting function names
6. **Tool Reference Bug** - Fixed tool instance references
7. **Missing Dependencies** - Added all required packages
8. **File Type Validation** - Added PDF file validation

### Inefficient Prompts Improved

1. **Agent Descriptions** - Made professional and experienced
2. **Task Descriptions** - Created structured analysis frameworks
3. **Expected Outputs** - Designed professional report formats
4. **Analysis Structure** - Added proper financial methodology

### New Features Added

1. **Queue Worker Model** - Redis + Celery for concurrent processing
2. **Database Integration** - SQLAlchemy for data persistence
3. **Enhanced API** - Status tracking, results retrieval, health checks
4. **Convenience Script** - Easy startup with `python run.py`

## File Structure

```
financial-document-analyzer-debug/
├── agents.py              # AI agents configuration
├── database.py            # Database models and operations
├── main.py               # FastAPI application
├── queue_worker.py       # Celery background tasks
├── task.py               # CrewAI task definitions
├── tools.py              # Document processing tools
├── run.py                # Convenience startup script
├── requirements.txt      # Dependencies
├── README.md             # This documentation
└── data/
    └── TSLA-Q2-2025-Update.pdf  # Sample document
```

## Dependencies

- crewai
- crewai-tools
- fastapi
- uvicorn
- langchain
- langchain-openai
- langchain-community
- openai
- sqlalchemy
- redis
- celery
- python-dotenv
- python-multipart

## Environment Variables

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
DATABASE_URL=sqlite:///./financial_analyzer.db
REDIS_URL=redis://localhost:6379/0
```

## Usage Examples

### Python Client
```python
import requests

# Upload and analyze document
with open('financial_report.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/analyze',
        files={'file': f},
        data={'query': 'Analyze this quarterly report for investment opportunities'}
    )

task_id = response.json()['task_id']

# Check status
status_response = requests.get(f'http://localhost:8000/task/{task_id}')
print(status_response.json())

# Get results when completed
if status_response.json()['status'] == 'COMPLETED':
    result_response = requests.get(f'http://localhost:8000/task/{task_id}/result')
    print(result_response.json())
```

### cURL Examples
```bash
# Upload document
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@financial_report.pdf" \
  -F "query=Analyze this document for investment insights"

# Check status
curl "http://localhost:8000/task/{task_id}"

# Get result
curl "http://localhost:8000/task/{task_id}/result"
```

## Technical Details

### Database Schema
The system uses SQLAlchemy with SQLite (default) or PostgreSQL for data persistence. The main table `analysis_results` stores:
- Task metadata (ID, file name, query)
- Analysis results and status
- Timestamps and error messages
- Extracted financial metrics

### Queue Processing
Celery workers handle background processing of analysis requests, allowing for:
- Concurrent request handling
- Scalable processing
- Task status tracking
- Automatic retry on failure

### API Design
RESTful API with comprehensive endpoints for:
- Document upload and analysis
- Task status monitoring
- Result retrieval
- Health checks and monitoring

## Troubleshooting

### Common Issues

1. **Redis Connection Error**
   - Ensure Redis server is running: `redis-server`
   - Check Redis URL in `.env` file

2. **Celery Worker Not Starting**
   - Check Redis connection
   - Verify all dependencies are installed
   - Check worker logs for errors

3. **OpenAI API Errors**
   - Verify API key in `.env` file
   - Check API quota and billing

4. **File Upload Issues**
   - Ensure file is PDF format
   - Check file size limits
   - Verify data directory permissions
