from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
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
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@yournewsletter.com")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")



# Available categories
AVAILABLE_CATEGORIES = [
    "technology", "business", "sports", "health", 
    "entertainment", "science", "politics"
]

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
        Write a self-contained summary of the following news article in 2-3 sentences. 
        Do not mention that you are summarizing, do not reference the title or content explicitly, and do not include phrases like "based on the article." 
        Focus only on the main argument, discussion, and key points.

        Title: {title}
        Content: {content}

        Summary:
        """

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={GEMINI_API_KEY}"
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

def generate_newsletter_html(user_name: Optional[str], articles_by_category: dict) -> str:
    """Generate HTML newsletter content."""
    greeting = f"Hello {user_name}," if user_name else "Hello,"
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Personalized Newsletter</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px; }}
        .category {{ margin: 30px 0; }}
        .category h2 {{ color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; text-transform: capitalize; }}
        .article {{ background: #f9f9f9; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #667eea; }}
        .article h3 {{ margin: 0 0 10px 0; color: #333; }}
        .article a {{ color: #667eea; text-decoration: none; font-weight: bold; }}
        .article a:hover {{ text-decoration: underline; }}
        .summary {{ color: #666; margin: 10px 0; }}
        .footer {{ text-align: center; margin-top: 40px; padding: 20px; background: #f0f0f0; border-radius: 8px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🗞️ Your AI-Powered Newsletter</h1>
        <p>{greeting}</p>
        <p>Here's your personalized news digest from the past week!</p>
    </div>
'''
    for category, articles in articles_by_category.items():
        if not articles:
            continue
        html_content += f'''
    <div class="category">
        <h2>{category.title()}</h2>
'''
        for article in articles:
            title = article.get("title", "No title")
            url = article.get("url", "#")
            description = article.get("description", "")
            html_content += f'''
        <div class="article">
            <h3><a href="{url}" target="_blank">{title}</a></h3>
            <div class="summary">{description}</div>
        </div>
'''
        html_content += "    </div>"
    html_content += '''
    <div class="footer">
        <p>Thanks for trying our AI-Powered Newsletter Service! 🚀</p>
        <p>This was your one-time personalized newsletter. We hope you found it valuable!</p>
        <p><small>This newsletter was generated using AI and the latest news APIs.</small></p>
    </div>
</body>
</html>
'''
    return html_content

async def send_email(to_email: str, subject: str, html_content: str):
    """Send email SMTP."""
    try:
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email

        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(FROM_EMAIL, GMAIL_PASSWORD)
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        return True
    except Exception as smtp_error:
        print(f"SMTP fallback failed: {smtp_error}")
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
        # Create user
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            categories=",".join(user_data.categories),
            newsletter_sent=False
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Fetch news
        articles_by_category = await fetch_news_articles(user_data.categories)

        # Summarize each article using Gemini
        for category, articles in articles_by_category.items():
            for article in articles:
                title = article.get("title", "")
                content = article.get("content") or article.get("description") or ""
                summary = await summarize_article(title, content)
                article["description"] = summary

        # Generate newsletter HTML
        html_content = generate_newsletter_html(user_data.name, articles_by_category)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)