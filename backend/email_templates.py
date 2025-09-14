from typing import Dict, List, Optional
from datetime import datetime

def generate_newsletter_template(
    user_name: Optional[str], 
    articles_by_category: Dict[str, List[dict]], 
    total_articles: int = 0
) -> str:
    """
    Generate a professional newsletter HTML template
    
    Args:
        user_name: Optional user name for personalization
        articles_by_category: Dictionary of category -> list of articles
        total_articles: Total number of articles in the newsletter
    
    Returns:
        HTML string for the newsletter
    """
    
    greeting = f"Hello {user_name}," if user_name else "Hello!"
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # CSS styles
    css_styles = """
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333333;
            max-width: 600px;
            margin: 0 auto;
            padding: 0;
            background-color: #f8fafc;
        }
        .container {
            background-color: #ffffff;
            margin: 20px;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0 0 10px 0;
            font-size: 28px;
            font-weight: 700;
        }
        .header p {
            margin: 0;
            font-size: 16px;
            opacity: 0.9;
        }
        .content {
            padding: 30px;
        }
        .stats {
            background: #f1f5f9;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
            text-align: center;
        }
        .stats-item {
            display: inline-block;
            margin: 0 15px;
            text-align: center;
        }
        .stats-number {
            display: block;
            font-size: 24px;
            font-weight: 700;
            color: #667eea;
        }
        .stats-label {
            font-size: 12px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .category {
            margin: 40px 0;
        }
        .category-header {
            color: #1e293b;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            text-transform: capitalize;
            display: flex;
            align-items: center;
        }
        .category-emoji {
            font-size: 24px;
            margin-right: 10px;
        }
        .article {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .article:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .article h3 {
            margin: 0 0 12px 0;
            font-size: 18px;
            font-weight: 600;
            color: #1e293b;
            line-height: 1.4;
        }
        .article a {
            color: #1e293b;
            text-decoration: none;
        }
        .article a:hover {
            color: #667eea;
            text-decoration: underline;
        }
        .summary {
            color: #475569;
            font-size: 14px;
            line-height: 1.5;
            margin-bottom: 12px;
        }
        .article-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid #f1f5f9;
        }
        .source {
            font-size: 12px;
            color: #64748b;
            font-weight: 500;
        }
        .read-more {
            font-size: 12px;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }
        .read-more:hover {
            text-decoration: underline;
        }
        .footer {
            background: #f8fafc;
            padding: 30px;
            text-align: center;
            border-top: 1px solid #e2e8f0;
        }
        .footer h3 {
            color: #1e293b;
            margin: 0 0 15px 0;
            font-size: 18px;
        }
        .footer p {
            color: #64748b;
            margin: 10px 0;
            font-size: 14px;
        }
        .ai-badge {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 10px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-left: 8px;
        }
        .divider {
            height: 1px;
            background: linear-gradient(to right, transparent, #e2e8f0, transparent);
            margin: 30px 0;
        }
    </style>
    """
    
    # Category emojis
    category_emojis = {
        'technology': '💻',
        'business': '💼',
        'sports': '⚽',
        'health': '🏥',
        'entertainment': '🎬',
        'science': '🔬',
        'politics': '🏛️'
    }
    
    # Start building HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your AI-Powered Newsletter</title>
        {css_styles}
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🗞️ Your AI Newsletter</h1>
                <p>{greeting}</p>
                <p>Your personalized news digest • {current_date}</p>
            </div>
            
            <div class="content">
                <div class="stats">
                    <div class="stats-item">
                        <span class="stats-number">{total_articles}</span>
                        <span class="stats-label">Articles</span>
                    </div>
                    <div class="stats-item">
                        <span class="stats-number">{len(articles_by_category)}</span>
                        <span class="stats-label">Categories</span>
                    </div>
                    <div class="stats-item">
                        <span class="stats-number">7</span>
                        <span class="stats-label">Days</span>
                    </div>
                </div>
    """
    
    # Add articles by category
    for category, articles in articles_by_category.items():
        if not articles:
            continue
            
        emoji = category_emojis.get(category, '📰')
        
        html_content += f"""
                <div class="category">
                    <h2 class="category-header">
                        <span class="category-emoji">{emoji}</span>
                        {category.title()}
                    </h2>
        """
        
        for article in articles:
            title = article.get("title", "No title available")
            url = article.get("url", "#")
            description = article.get("description", "No summary available")
            source = article.get("source", {}).get("name", "Unknown source")
            
            # Truncate long descriptions
            if len(description) > 200:
                description = description[:197] + "..."
            
            html_content += f"""
                    <div class="article">
                        <h3><a href="{url}" target="_blank">{title}</a></h3>
                        <div class="summary">{description}<span class="ai-badge">AI Summary</span></div>
                        <div class="article-meta">
                            <span class="source">📰 {source}</span>
                            <a href="{url}" target="_blank" class="read-more">Read Full Article →</a>
                        </div>
                    </div>
            """
        
        html_content += "</div>"
    
    # Add footer
    html_content += f"""
            </div>
            
            <div class="divider"></div>
            
            <div class="footer">
                <h3>Thanks for trying our AI Newsletter! 🚀</h3>
                <p>This personalized newsletter was generated using the latest AI technology and news APIs.</p>
                <p>Each article summary was crafted by AI to give you the most important insights quickly.</p>
                <p><strong>This was your one-time newsletter.</strong> We hope you found it valuable!</p>
                <p style="margin-top: 20px; font-size: 12px; color: #94a3b8;">
                    Generated on {current_date} • Powered by AI • No spam, ever.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content


def generate_welcome_email(user_name: Optional[str], user_email: str) -> str:
    """Generate a simple welcome email confirmation"""
    
    greeting = f"Hello {user_name}," if user_name else "Hello!"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Welcome to AI Newsletter</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #667eea; color: white; padding: 20px; text-align: center; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Welcome to AI Newsletter! 🎉</h1>
        </div>
        <div style="padding: 20px;">
            <p>{greeting}</p>
            <p>Thank you for registering for our AI-powered newsletter service!</p>
            <p>We're currently generating your personalized newsletter and it will arrive in your inbox shortly.</p>
            <p>What to expect:</p>
            <ul>
                <li>🤖 AI-summarized articles from your selected categories</li>
                <li>📰 Latest news from the past week</li>
                <li>⚡ Delivered instantly to your inbox</li>
            </ul>
            <p>Best regards,<br>The AI Newsletter Team</p>
        </div>
    </body>
    </html>
    """