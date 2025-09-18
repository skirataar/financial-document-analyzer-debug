import os
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import create_engine, Column, String, Text, DateTime, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./financial_analyzer.db')
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AnalysisResult(Base):
    """Model for storing financial analysis results"""
    __tablename__ = "analysis_results"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String, unique=True, nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    query = Column(Text, nullable=False)
    analysis_result = Column(Text, nullable=True)
    status = Column(String, nullable=False)  # PENDING, IN_PROGRESS, COMPLETED, FAILED
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Financial metrics (extracted from analysis)
    revenue = Column(Float, nullable=True)
    profit_margin = Column(Float, nullable=True)
    debt_ratio = Column(Float, nullable=True)
    pe_ratio = Column(Float, nullable=True)
    investment_recommendation = Column(String, nullable=True)  # BUY, HOLD, SELL
    risk_level = Column(String, nullable=True)  # LOW, MEDIUM, HIGH
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'file_name': self.file_name,
            'query': self.query,
            'analysis_result': self.analysis_result,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message,
            'revenue': self.revenue,
            'profit_margin': self.profit_margin,
            'debt_ratio': self.debt_ratio,
            'pe_ratio': self.pe_ratio,
            'investment_recommendation': self.investment_recommendation,
            'risk_level': self.risk_level
        }

class UserSession(Base):
    """Model for storing user sessions and preferences"""
    __tablename__ = "user_sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, unique=True, nullable=False)
    user_agent = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'user_agent': self.user_agent,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'is_active': self.is_active
        }

# Create tables
def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database operations
class DatabaseManager:
    """Manager class for database operations"""
    
    def __init__(self):
        self.engine = engine
        self.db = SessionLocal()
    
    def create_analysis_result(self, task_id: str, file_name: str, file_path: str, 
                             query: str, status: str = "PENDING") -> AnalysisResult:
        """Create a new analysis result record"""
        result = AnalysisResult(
            task_id=task_id,
            file_name=file_name,
            file_path=file_path,
            query=query,
            status=status
        )
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)
        return result
    
    def update_analysis_result(self, task_id: str, analysis_result: str = None, 
                             status: str = None, error_message: str = None,
                             **financial_metrics) -> Optional[AnalysisResult]:
        """Update an analysis result record"""
        result = self.db.query(AnalysisResult).filter(AnalysisResult.task_id == task_id).first()
        if result:
            if analysis_result is not None:
                result.analysis_result = analysis_result
            if status is not None:
                result.status = status
            if error_message is not None:
                result.error_message = error_message
            if status == "COMPLETED":
                result.completed_at = datetime.utcnow()
            
            # Update financial metrics
            for key, value in financial_metrics.items():
                if hasattr(result, key):
                    setattr(result, key, value)
            
            self.db.commit()
            self.db.refresh(result)
        return result
    
    def get_analysis_result(self, task_id: str) -> Optional[AnalysisResult]:
        """Get analysis result by task ID"""
        return self.db.query(AnalysisResult).filter(AnalysisResult.task_id == task_id).first()
    
    def get_analysis_results(self, limit: int = 100, offset: int = 0) -> list[AnalysisResult]:
        """Get paginated analysis results"""
        return self.db.query(AnalysisResult).offset(offset).limit(limit).all()
    
    def create_user_session(self, session_id: str, user_agent: str = None, 
                          ip_address: str = None) -> UserSession:
        """Create a new user session"""
        session = UserSession(
            session_id=session_id,
            user_agent=user_agent,
            ip_address=ip_address
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def update_user_session(self, session_id: str) -> Optional[UserSession]:
        """Update user session last activity"""
        session = self.db.query(UserSession).filter(UserSession.session_id == session_id).first()
        if session:
            session.last_activity = datetime.utcnow()
            self.db.commit()
            self.db.refresh(session)
        return session
    
    def get_session(self):
        """Get a new database session"""
        return self.db
    
    def close(self):
        """Close database connection"""
        self.db.close()

# Initialize database
create_tables()
