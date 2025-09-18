import os
from typing import Dict, Any
from celery import Celery
from dotenv import load_dotenv

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document, investment_analysis, risk_assessment, verification

load_dotenv()

# Initialize Celery
celery_app = Celery(
    'financial_analyzer',
    broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0')
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes
    task_soft_time_limit=240,  # 4 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
)

@celery_app.task(bind=True, name='analyze_financial_document_task')
def analyze_financial_document_task(self, query: str, file_path: str) -> Dict[str, Any]:
    """
    Celery task to process financial document analysis
    
    Args:
        query: User's analysis query
        file_path: Path to the uploaded PDF file
        
    Returns:
        Dict containing analysis results
    """
    try:
        # Update task progress
        self.update_state(state='PROGRESS', meta={'status': 'Starting analysis...'})
        
        # Add tools to tasks at runtime
        from tools import financial_document_tool, search_tool
        
        # Add tools to tasks
        analyze_financial_document.tools = [financial_document_tool, search_tool]
        investment_analysis.tools = [financial_document_tool, search_tool]
        risk_assessment.tools = [financial_document_tool, search_tool]
        verification.tools = [financial_document_tool]
        
        # Create financial analysis crew
        financial_crew = Crew(
            agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
            tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
            process=Process.sequential,
            verbose=True
        )
        
        # Update task progress
        self.update_state(state='PROGRESS', meta={'status': 'Running financial analysis...'})
        
        # Execute the crew
        result = financial_crew.kickoff(inputs={'query': query, 'file_path': file_path})
        
        # Update task progress
        self.update_state(state='PROGRESS', meta={'status': 'Finalizing results...'})
        
        return {
            'status': 'SUCCESS',
            'query': query,
            'file_path': file_path,
            'analysis': str(result),
            'task_id': self.request.id
        }
        
    except Exception as e:
        # Update task state with error
        self.update_state(
            state='FAILURE',
            meta={'status': 'Error occurred', 'error': str(e)}
        )
        raise e

@celery_app.task(name='cleanup_file_task')
def cleanup_file_task(file_path: str) -> Dict[str, Any]:
    """
    Celery task to clean up uploaded files after processing
    
    Args:
        file_path: Path to the file to be deleted
        
    Returns:
        Dict containing cleanup status
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return {'status': 'SUCCESS', 'message': f'File {file_path} cleaned up successfully'}
        else:
            return {'status': 'WARNING', 'message': f'File {file_path} not found'}
    except Exception as e:
        return {'status': 'ERROR', 'message': f'Error cleaning up file: {str(e)}'}

# Health check task
@celery_app.task(name='health_check_task')
def health_check_task() -> Dict[str, Any]:
    """Health check task for the queue worker"""
    return {
        'status': 'HEALTHY',
        'message': 'Queue worker is running properly',
        'worker_id': os.getenv('HOSTNAME', 'unknown')
    }

if __name__ == '__main__':
    # Start the Celery worker
    celery_app.start()
