from app import app
from flask import request, redirect

# Force HTTPS
@app.before_request
def before_request():
    if not request.is_secure and app.env != 'development':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

if __name__ == "__main__":
    app.run() 