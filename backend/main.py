# backend/main.py
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os
from datetime import datetime, timedelta
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from dotenv import load_dotenv
import re
import hashlib
import secrets
from email_templates import generate_newsletter_html, generate_unsubscribe_success_html, generate_unsubscribe_error_html

load_dotenv()

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./newsletter.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    categories = Column(Text, nullable=False)  # JSON string
    newsletter_sent = Column(Boolean, default=False)
    unsubscribe_token = Column(String, unique=True, nullable=False)  # New field for unsubscribe
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Pydantic models
class UserRegistration(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    categories: List[str]

class UserResponse(BaseModel):
    id: int
    name: Optional[str]
    email: str
    categories: List[str]
    newsletter_sent: bool
    created_at: datetime

# FastAPI app
app = FastAPI(title="AI Newsletter Service")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configuration
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "your_news_api_key")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_api_key")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "your_sendgrid_api_key")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")  # For unsubscribe links

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

# Available categories
AVAILABLE_CATEGORIES = [
    "technology", "business", "sports", "health", 
    "entertainment", "science", "politics"
]

def generate_unsubscribe_token() -> str:
    """Generate a secure unsubscribe token."""
    return secrets.token_urlsafe(32)

def validate_email(email: str) -> bool:
    """Simple email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

async def fetch_news_articles(categories: List[str], days_back: int = 7) -> dict:
    """Fetch news articles from NewsAPI"""
    articles_by_category = {}
    
    # Calculate date range
    to_date = datetime.now()
    from_date = to_date - timedelta(days=days_back)
    
    for category in categories:
        if category not in AVAILABLE_CATEGORIES:
            continue
            
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": NEWS_API_KEY,
            "category": category,
            "language": "en",
            "country": "us",
            "from": from_date.strftime("%Y-%m-%d"),
            "to": to_date.strftime("%Y-%m-%d"),
            "pageSize": 5
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])[:3]  # Top 3 articles per category
                articles_by_category[category] = articles
        except Exception as e:
            print(f"Error fetching news for {category}: {e}")
            articles_by_category[category] = []
    
    return articles_by_category

async def summarize_article(title: str, content: str) -> str:
    """Summarize article using Gemini API."""
    # Truncate content if too long
    max_content_length = 2000
    try:
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."

        prompt = f"""
Please provide a concise 3-4 sentence summary of the following news article.\n\nTitle: {title}\nContent: {content}\n\nSummary:"""

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            summary = result["candidates"][0]["content"]["parts"][0]["text"]
            return summary.strip()
        else:
            print(f"Gemini API error: {response.status_code} {response.text}")
            return f"Summary unavailable. {title}"
    except Exception as e:
        print(f"Error summarizing article: {e}")
        return f"Summary unavailable. {title}"

async def send_email(to_email: str, subject: str, html_content: str):
    """Send email using Gmail SMTP."""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = GMAIL_USER
        msg['To'] = to_email

        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())
        return True
    except Exception as smtp_error:
        print(f"SMTP failed: {smtp_error}")
        return False

@app.get("/")
async def root():
    return {"message": "AI Newsletter Service API"}

@app.get("/categories")
async def get_categories():
    """Get available news categories."""
    return {"categories": AVAILABLE_CATEGORIES}

@app.post("/register", response_model=UserResponse)
async def register_user(user_data: UserRegistration, db: Session = Depends(get_db)):
    """Register a new user and send newsletter."""
    
    # Validate email
    if not validate_email(user_data.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Validate categories
    invalid_categories = [cat for cat in user_data.categories if cat not in AVAILABLE_CATEGORIES]
    if invalid_categories:
        raise HTTPException(status_code=400, detail=f"Invalid categories: {invalid_categories}")
    
    if not user_data.categories:
        raise HTTPException(status_code=400, detail="At least one category must be selected")
    
    try:
        # Generate unsubscribe token
        unsubscribe_token = generate_unsubscribe_token()
        
        # Create user
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            categories=",".join(user_data.categories),
            newsletter_sent=False,
            unsubscribe_token=unsubscribe_token
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Fetch news and generate newsletter
        articles_by_category = await fetch_news_articles(user_data.categories)
        
        # Create unsubscribe URL
        unsubscribe_url = f"{BASE_URL}/unsubscribe/{unsubscribe_token}"
        
        # Generate newsletter HTML using template
        html_content = generate_newsletter_html(user_data.name, articles_by_category, unsubscribe_url)
        
        # Send email
        subject = "Your Personalized AI Newsletter 📰"
        email_sent = await send_email(user_data.email, subject, html_content)
        
        if email_sent:
            # Mark as sent
            db_user.newsletter_sent = True
            db.commit()
        
        return UserResponse(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            categories=user_data.categories,
            newsletter_sent=db_user.newsletter_sent,
            created_at=db_user.created_at
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user details."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        categories=user.categories.split(","),
        newsletter_sent=user.newsletter_sent,
        created_at=user.created_at
    )

@app.get("/unsubscribe/{token}", response_class=HTMLResponse)
async def unsubscribe_user(token: str, db: Session = Depends(get_db)):
    """Unsubscribe user and delete their data."""
    try:
        # Find user by unsubscribe token
        user = db.query(User).filter(User.unsubscribe_token == token).first()
        
        if not user:
            # User not found - show error page
            error_html = generate_unsubscribe_error_html("Invalid or expired unsubscribe link.")
            return HTMLResponse(content=error_html, status_code=404)
        
        # Store email for confirmation page
        user_email = user.email
        
        # Delete user data
        db.delete(user)
        db.commit()
        
        # Show success page
        success_html = generate_unsubscribe_success_html(user_email)
        return HTMLResponse(content=success_html, status_code=200)
        
    except Exception as e:
        print(f"Error during unsubscribe: {e}")
        db.rollback()
        error_html = generate_unsubscribe_error_html("An error occurred while processing your request.")
        return HTMLResponse(content=error_html, status_code=500)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)