from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import os
import uuid
from typing import Dict, Any
from datetime import datetime

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document, investment_analysis, risk_assessment, verification
from database import DatabaseManager
from queue_worker import analyze_financial_document_task, cleanup_file_task

# Initialize FastAPI app
app = FastAPI(title="Financial Document Analyzer", version="1.0.0")

def run_crew(query: str, file_path: str = "data/sample.pdf") -> Dict[str, Any]:
    """Run the financial analysis crew"""
    from tools import financial_document_tool, search_tool
    
    # Add tools to tasks
    analyze_financial_document.tools = [financial_document_tool, search_tool]
    investment_analysis.tools = [financial_document_tool, search_tool]
    risk_assessment.tools = [financial_document_tool, search_tool]
    verification.tools = [financial_document_tool]
    
    financial_crew = Crew(
        agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
        tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
        process=Process.sequential,
        verbose=True
    )
    
    result = financial_crew.kickoff(inputs={'query': query, 'file_path': file_path})
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Financial Document Analyzer API is running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    try:
        # Check database connection
        db_manager = DatabaseManager()
        db_manager.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "queue": "available",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )

@app.post("/analyze")
async def analyze_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights"),
    use_queue: bool = Form(default=True)
):
    """Analyze financial document and provide comprehensive investment recommendations"""
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate query
        if not query or query.strip() == "":
            query = "Analyze this financial document for investment insights"
        
        # Initialize database manager
        db_manager = DatabaseManager()
        
        if use_queue:
            # Use queue worker for processing
            task = analyze_financial_document_task.delay(query.strip(), file_path)
            
            # Create database record
            analysis_result = db_manager.create_analysis_result(
                task_id=task.id,
                file_name=file.filename,
                file_path=file_path,
                query=query.strip(),
                status="PENDING"
            )
            
            # Schedule cleanup task
            background_tasks.add_task(cleanup_file_task, file_path)
            
            return {
                "status": "queued",
                "task_id": task.id,
                "query": query,
                "file_processed": file.filename,
                "file_id": file_id,
                "message": "Analysis queued for processing. Use the task_id to check status."
            }
        else:
            # Process synchronously (for testing)
            response = run_crew(query=query.strip(), file_path=file_path)
            
            # Create database record
            analysis_result = db_manager.create_analysis_result(
                task_id=str(uuid.uuid4()),
                file_name=file.filename,
                file_path=file_path,
                query=query.strip(),
                status="COMPLETED"
            )
            
            # Update with results
            db_manager.update_analysis_result(
                task_id=analysis_result.task_id,
                analysis_result=str(response),
                status="COMPLETED"
            )
            
            # Clean up file
            background_tasks.add_task(cleanup_file_task, file_path)
            
            return {
                "status": "success",
                "query": query,
                "analysis": str(response),
                "file_processed": file.filename,
                "file_id": file_id,
                "task_id": analysis_result.task_id
            }
        
    except Exception as e:
        # Update database with error if record exists
        try:
            db_manager = DatabaseManager()
            db_manager.update_analysis_result(
                task_id=file_id,
                status="FAILED",
                error_message=str(e)
            )
            db_manager.close()
        except:
            pass
        
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    
    finally:
        if 'db_manager' in locals():
            db_manager.close()

@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """Get the status of a specific analysis task"""
    try:
        db_manager = DatabaseManager()
        result = db_manager.get_analysis_result(task_id)
        db_manager.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return result.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving task status: {str(e)}")

@app.get("/results")
async def get_analysis_results(limit: int = 10, offset: int = 0):
    """Get paginated analysis results"""
    try:
        db_manager = DatabaseManager()
        results = db_manager.get_analysis_results(limit=limit, offset=offset)
        db_manager.close()
        
        return {
            "results": [result.to_dict() for result in results],
            "count": len(results),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving results: {str(e)}")

@app.get("/task/{task_id}/result")
async def get_task_result(task_id: str):
    """Get the analysis result for a completed task"""
    try:
        db_manager = DatabaseManager()
        result = db_manager.get_analysis_result(task_id)
        db_manager.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")
        
        if result.status != "COMPLETED":
            return {
                "status": result.status,
                "message": "Task not completed yet",
                "error": result.error_message
            }
        
        return {
            "status": "success",
            "task_id": task_id,
            "analysis": result.analysis_result,
            "financial_metrics": {
                "revenue": result.revenue,
                "profit_margin": result.profit_margin,
                "debt_ratio": result.debt_ratio,
                "pe_ratio": result.pe_ratio,
                "investment_recommendation": result.investment_recommendation,
                "risk_level": result.risk_level
            },
            "completed_at": result.completed_at.isoformat() if result.completed_at else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving task result: {str(e)}")

@app.delete("/task/{task_id}")
async def delete_task(task_id: str):
    """Delete a task and its associated data"""
    try:
        db_manager = DatabaseManager()
        result = db_manager.get_analysis_result(task_id)
        
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Delete from database
        db_manager.db.delete(result)
        db_manager.db.commit()
        db_manager.close()
        
        return {"status": "success", "message": f"Task {task_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)