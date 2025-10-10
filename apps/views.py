from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    """Simple homepage view"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Spa Central - Home</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                margin: 0;
            }
            .container {
                text-align: center;
                background: rgba(255, 255, 255, 0.1);
                padding: 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
            }
            h1 { font-size: 3em; margin-bottom: 20px; }
            p { font-size: 1.2em; margin-bottom: 30px; }
            .api-link {
                color: white;
                text-decoration: none;
                background: rgba(255, 255, 255, 0.2);
                padding: 10px 20px;
                border-radius: 25px;
                display: inline-block;
                margin: 10px;
                transition: all 0.3s ease;
            }
            .api-link:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏊‍♀️ Spa Central</h1>
            <p>Welcome to Spa Central Management System</p>
            <a href="/admin/" class="api-link">Admin Panel</a>
            <a href="/api/" class="api-link">API Documentation</a>
            <a href="/health/" class="api-link">Health Check</a>
        </div>
    </body>
    </html>
    """)

def custom_404(request, exception=None):
    """Custom 404 handler"""
    return render(request, '404.html', status=404)

def custom_500(request):
    """Custom 500 handler"""
    return render(request, '500.html', status=500)
