from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class RequestLog(Base):
    __tablename__ = 'request_logs'
    id = Column(Integer, primary_key=True)
    endpoint = Column(String, nullable=False)
    params = Column(String)
    result = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)