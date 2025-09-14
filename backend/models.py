from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model for newsletter subscribers"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    categories = Column(Text, nullable=False)  # Comma-separated list of categories
    newsletter_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    newsletters = relationship("Newsletter", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', categories='{self.categories}')>"


class Newsletter(Base):
    """Newsletter model to store generated newsletters"""
    __tablename__ = "newsletters"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(255), nullable=False)
    html_content = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    email_status = Column(String(50), default="sent")  # sent, failed, pending
    
    # Relationships
    user = relationship("User", back_populates="newsletters")
    articles = relationship("NewsArticle", back_populates="newsletter")
    
    def __repr__(self):
        return f"<Newsletter(id={self.id}, user_id={self.user_id}, subject='{self.subject[:50]}...')>"


class NewsArticle(Base):
    """News article model to store fetched and summarized articles"""
    __tablename__ = "news_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    newsletter_id = Column(Integer, ForeignKey("newsletters.id"), nullable=False)
    title = Column(String(500), nullable=False)
    url = Column(Text, nullable=False)
    source = Column(String(100), nullable=True)
    category = Column(String(50), nullable=False)
    original_content = Column(Text, nullable=True)
    ai_summary = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    newsletter = relationship("Newsletter", back_populates="articles")
    
    def __repr__(self):
        return f"<NewsArticle(id={self.id}, title='{self.title[:50]}...', category='{self.category}')>"


class APIUsage(Base):
    """Track API usage for monitoring and billing"""
    __tablename__ = "api_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    service = Column(String(50), nullable=False)  # 'news_api', 'openai', 'sendgrid'
    endpoint = Column(String(100), nullable=True)
    requests_count = Column(Integer, default=1)
    tokens_used = Column(Integer, nullable=True)  # For OpenAI
    cost = Column(String(20), nullable=True)  # Estimated cost
    date = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<APIUsage(service='{self.service}', requests={self.requests_count}, date='{self.date}')>"