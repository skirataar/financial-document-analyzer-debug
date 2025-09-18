#!/usr/bin/env python3
"""
Simple script to run the Financial Document Analyzer
"""

import subprocess
import sys
import os

def main():
    print("Starting Financial Document Analyzer...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  .env file not found. Please create one with your API keys:")
        print("   OPENAI_API_KEY=your_key_here")
        print("   SERPER_API_KEY=your_key_here")
        print()
        print("You can also run without .env for testing (will use synchronous mode)")
        print()
    
    # Start the FastAPI server
    try:
        print("🚀 Starting FastAPI server on http://localhost:8000")
        print("📖 API documentation available at http://localhost:8000/docs")
        print("🛑 Press Ctrl+C to stop")
        print()
        
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
