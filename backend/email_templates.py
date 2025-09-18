from typing import Optional, Dict, List

def generate_newsletter_html(user_name: Optional[str], articles_by_category: Dict, unsubscribe_url: str) -> str:
    """Generate HTML newsletter content with unsubscribe link."""
    greeting = f"Hello {user_name}," if user_name else "Hello,"
    
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Personalized Newsletter</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            line-height: 1.6; 
            color: #333; 
            max-width: 600px; 
            margin: 0 auto; 
            padding: 20px; 
            background-color: #f8fafc;
        }}
        .container {{
            background-color: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        }}
        .header {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 40px 30px; 
            text-align: center; 
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 28px;
            font-weight: 700;
        }}
        .header p {{
            margin: 5px 0;
            font-size: 16px;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
        }}
        .category {{ 
            margin: 35px 0; 
        }}
        .category:first-child {{
            margin-top: 0;
        }}
        .category h2 {{ 
            color: #667eea; 
            border-bottom: 3px solid #667eea; 
            padding-bottom: 12px; 
            text-transform: capitalize; 
            font-size: 24px;
            margin: 0 0 20px 0;
        }}
        .article {{ 
            background: #f8fafc; 
            padding: 25px; 
            margin: 20px 0; 
            border-radius: 10px; 
            border-left: 5px solid #667eea;
            transition: transform 0.2s ease;
        }}
        .article:hover {{
            transform: translateY(-2px);
        }}
        .article h3 {{ 
            margin: 0 0 12px 0; 
            color: #1a202c; 
            font-size: 18px;
            line-height: 1.4;
        }}
        .article a {{ 
            color: #667eea; 
            text-decoration: none; 
            font-weight: 600; 
        }}
        .article a:hover {{ 
            text-decoration: underline; 
            color: #5a67d8;
        }}
        .summary {{ 
            color: #4a5568; 
            margin: 12px 0 0 0; 
            font-size: 14px;
            line-height: 1.5;
        }}
        .footer {{ 
            text-align: center; 
            margin-top: 40px; 
            padding: 30px; 
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%); 
            border-radius: 10px; 
        }}
        .footer h3 {{
            color: #2d3748;
            margin: 0 0 15px 0;
            font-size: 20px;
        }}
        .footer p {{
            margin: 10px 0;
            color: #4a5568;
        }}
        .unsubscribe {{
            margin-top: 25px;
            padding-top: 20px;
            border-top: 1px solid #cbd5e0;
        }}
        .unsubscribe a {{
            color: #718096;
            text-decoration: none;
            font-size: 12px;
        }}
        .unsubscribe a:hover {{
            text-decoration: underline;
            color: #4a5568;
        }}
        .powered-by {{
            font-size: 11px;
            color: #a0aec0;
            margin-top: 15px;
        }}
        @media (max-width: 600px) {{
            body {{ padding: 10px; }}
            .header {{ padding: 25px 20px; }}
            .content {{ padding: 20px; }}
            .article {{ padding: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗞️ Your AI-Powered Newsletter</h1>
            <p>{greeting}</p>
            <p>Here's your personalized news digest from the past week!</p>
        </div>
        
        <div class="content">'''

    # Add articles by category
    for category, articles in articles_by_category.items():
        if not articles:
            continue
            
        html_content += f'''
            <div class="category">
                <h2>{category.title()}</h2>'''
        
        for article in articles:
            title = article.get("title", "No title")
            url = article.get("url", "#")
            description = article.get("description", "")
            
            html_content += f'''
                <div class="article">
                    <h3><a href="{url}" target="_blank">{title}</a></h3>
                    <div class="summary">{description}</div>
                </div>'''
        
        html_content += '''
            </div>'''

    html_content += f'''
        </div>
        
        <div class="footer">
            <h3>Thanks for trying our AI-Powered Newsletter Service! 🚀</h3>
            <p>This was your one-time personalized newsletter. We hope you found it valuable!</p>
            <p>Our AI curated the latest news from your selected categories and created personalized summaries just for you.</p>
            
            <div class="unsubscribe">
                <p><a href="{unsubscribe_url}" target="_blank">Click here to unsubscribe and remove your data</a></p>
            </div>
            
            <div class="powered-by">
                <p>This newsletter was generated using AI and the latest news APIs.</p>
            </div>
        </div>
    </div>
</body>
</html>'''

    return html_content


def generate_unsubscribe_success_html(user_email: str) -> str:
    """Generate HTML for successful unsubscribe confirmation."""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Successfully Unsubscribed</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            line-height: 1.6; 
            color: #333; 
            max-width: 500px; 
            margin: 0 auto; 
            padding: 40px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }}
        .success-icon {{
            width: 64px;
            height: 64px;
            background: #10b981;
            border-radius: 50%;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
        }}
        h1 {{
            color: #1f2937;
            margin: 0 0 15px 0;
            font-size: 24px;
        }}
        p {{
            color: #6b7280;
            margin: 10px 0;
        }}
        .email {{
            background: #f3f4f6;
            padding: 10px 15px;
            border-radius: 8px;
            margin: 15px 0;
            font-family: monospace;
            color: #374151;
        }}
        .note {{
            font-size: 14px;
            color: #9ca3af;
            margin-top: 25px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="success-icon">✓</div>
        <h1>Successfully Unsubscribed</h1>
        <p>Your email address has been successfully removed from our newsletter service.</p>
        <div class="email">{user_email}</div>
        <p>All your data has been permanently deleted from our database.</p>
        <div class="note">
            <p>Thank you for trying our AI-Powered Newsletter Service. If you change your mind, you can always register again on our homepage.</p>
        </div>
    </div>
</body>
</html>'''


def generate_unsubscribe_error_html(error_message: str = "User not found") -> str:
    """Generate HTML for unsubscribe error page."""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unsubscribe Error</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            line-height: 1.6; 
            color: #333; 
            max-width: 500px; 
            margin: 0 auto; 
            padding: 40px 20px;
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }}
        .error-icon {{
            width: 64px;
            height: 64px;
            background: #ef4444;
            border-radius: 50%;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            color: white;
        }}
        h1 {{
            color: #1f2937;
            margin: 0 0 15px 0;
            font-size: 24px;
        }}
        p {{
            color: #6b7280;
            margin: 10px 0;
        }}
        .error-message {{
            background: #fef2f2;
            border: 1px solid #fecaca;
            color: #b91c1c;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }}
        .note {{
            font-size: 14px;
            color: #9ca3af;
            margin-top: 25px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="error-icon">✗</div>
        <h1>Unsubscribe Failed</h1>
        <p>We encountered an issue while processing your unsubscribe request.</p>
        <div class="error-message">{error_message}</div>
        <div class="note">
            <p>If you continue to experience issues, the data may have already been removed or the link may have expired.</p>
        </div>
    </div>
</body>
</html>'''