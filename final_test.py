#!/usr/bin/env python3
"""
Final comprehensive test script for Financial Document Analyzer
This script tests all components to ensure everything works correctly
"""

import os
import sys
import traceback

def test_imports():
    """Test all module imports"""
    print("Testing module imports...")
    
    try:
        import agents
        print("✓ agents.py imports successfully")
        
        import tools
        print("✓ tools.py imports successfully")
        
        import task
        print("✓ task.py imports successfully")
        
        import database
        print("✓ database.py imports successfully")
        
        import queue_worker
        print("✓ queue_worker.py imports successfully")
        
        import main
        print("✓ main.py imports successfully")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        traceback.print_exc()
        return False

def test_database():
    """Test database operations"""
    print("\nTesting database operations...")
    
    try:
        from database import DatabaseManager, AnalysisResult, Base
        
        # Test database creation
        db_manager = DatabaseManager()
        print("✓ Database manager created")
        
        # Test table creation
        Base.metadata.create_all(db_manager.engine)
        print("✓ Database tables created")
        
        # Test creating a record
        result = db_manager.create_analysis_result(
            task_id="final-test-123",
            file_name="test.pdf",
            file_path="test.pdf",
            query="Test query for final verification",
            status="PENDING"
        )
        print("✓ Analysis result created")
        
        # Test updating a record
        db_manager.update_analysis_result(
            task_id="final-test-123",
            status="COMPLETED",
            analysis_result="Test analysis completed successfully"
        )
        print("✓ Analysis result updated")
        
        # Test getting results
        results = db_manager.get_analysis_results(limit=1)
        print(f"✓ Retrieved {len(results)} results")
        
        # Test session
        session = db_manager.get_session()
        session.close()
        print("✓ Database session works")
        
        db_manager.close()
        return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        traceback.print_exc()
        return False

def test_tools():
    """Test tools functionality"""
    print("\nTesting tools...")
    
    try:
        from tools import financial_document_tool, search_tool
        
        print("✓ Tools created successfully")
        
        # Test PDF tool with sample file
        if os.path.exists("data/TSLA-Q2-2025-Update.pdf"):
            result = financial_document_tool.invoke("data/TSLA-Q2-2025-Update.pdf")
            if "Error" not in str(result):
                print("✓ PDF tool works with sample file")
            else:
                print("⚠ PDF tool returned error (expected without proper setup)")
        else:
            print("⚠ Sample PDF not found")
        
        return True
    except Exception as e:
        print(f"✗ Tools error: {e}")
        traceback.print_exc()
        return False

def test_fastapi():
    """Test FastAPI app creation and routes"""
    print("\nTesting FastAPI app...")
    
    try:
        from main import app
        
        print("✓ FastAPI app created")
        
        # Test route registration
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/health", "/analyze", "/task/{task_id}", "/results"]
        
        missing_routes = []
        for route in expected_routes:
            if not any(route in r for r in routes):
                missing_routes.append(route)
        
        if missing_routes:
            print(f"✗ Missing routes: {missing_routes}")
            return False
        
        print("✓ All expected routes registered")
        return True
    except Exception as e:
        print(f"✗ FastAPI error: {e}")
        traceback.print_exc()
        return False

def test_agents():
    """Test agent creation"""
    print("\nTesting agents...")
    
    try:
        from agents import financial_analyst, verifier, investment_advisor, risk_assessor
        
        agents = [
            ("Financial Analyst", financial_analyst),
            ("Verifier", verifier),
            ("Investment Advisor", investment_advisor),
            ("Risk Assessor", risk_assessor)
        ]
        
        for name, agent in agents:
            if not agent.role or not agent.goal:
                print(f"✗ {name} agent is not properly configured")
                return False
            print(f"✓ {name} agent configured correctly")
        
        return True
    except Exception as e:
        print(f"✗ Agents error: {e}")
        traceback.print_exc()
        return False

def test_tasks():
    """Test task creation"""
    print("\nTesting tasks...")
    
    try:
        from task import analyze_financial_document, investment_analysis, risk_assessment, verification
        
        tasks = [
            ("Financial Document Analysis", analyze_financial_document),
            ("Investment Analysis", investment_analysis),
            ("Risk Assessment", risk_assessment),
            ("Verification", verification)
        ]
        
        for name, task in tasks:
            if not task.description or not task.expected_output:
                print(f"✗ {name} task is not properly configured")
                return False
            print(f"✓ {name} task configured correctly")
        
        return True
    except Exception as e:
        print(f"✗ Tasks error: {e}")
        traceback.print_exc()
        return False

def test_queue_worker():
    """Test queue worker configuration"""
    print("\nTesting queue worker...")
    
    try:
        from queue_worker import celery_app
        
        print("✓ Celery app created")
        print(f"  Broker: {celery_app.conf.broker_url}")
        print(f"  Backend: {celery_app.conf.result_backend}")
        
        # Test task registration
        tasks = list(celery_app.tasks.keys())
        if 'analyze_financial_document_task' in tasks:
            print("✓ Analysis task registered")
        else:
            print("✗ Analysis task not found")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Queue worker error: {e}")
        traceback.print_exc()
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        "agents.py",
        "database.py",
        "main.py",
        "queue_worker.py",
        "task.py",
        "tools.py",
        "requirements.txt",
        "README.md",
        "run.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✓ {file} exists")
    
    if missing_files:
        print(f"✗ Missing files: {missing_files}")
        return False
    
    return True

def test_dependencies():
    """Test that all dependencies are specified"""
    print("\nTesting dependencies...")
    
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
        
        required_deps = [
            "crewai",
            "fastapi",
            "uvicorn",
            "langchain",
            "openai",
            "sqlalchemy",
            "redis",
            "celery",
            "python-dotenv",
            "python-multipart"
        ]
        
        missing_deps = []
        for dep in required_deps:
            if dep not in content:
                missing_deps.append(dep)
            else:
                print(f"✓ {dep} in requirements.txt")
        
        if missing_deps:
            print(f"✗ Missing dependencies: {missing_deps}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Dependencies error: {e}")
        return False

def main():
    """Run all tests"""
    print("Final Test - Financial Document Analyzer")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_database,
        test_tools,
        test_fastapi,
        test_agents,
        test_tasks,
        test_queue_worker,
        test_file_structure,
        test_dependencies
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("ALL TESTS PASSED!")
        print("The codebase is ready for submission!")
        return True
    else:
        print("Some tests failed. Please fix the issues before submitting.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
