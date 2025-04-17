from flask import Flask, send_from_directory, send_file, url_for
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Create Flask app with production config
app = Flask(__name__)
app.config.update(
    ENV='production',
    DEBUG=False,
    PROPAGATE_EXCEPTIONS=True,
    SERVER_NAME='kcc-flipbook.onrender.com',
    PREFERRED_URL_SCHEME='https'
)

# Ensure directories exist
for directory in ['output', 'turnjs']:
    if not os.path.exists(directory):
        os.makedirs(directory)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    try:
        logger.info(f"Requested path: {path}")
        
        # Serve flipbook.html at root
        if not path:
            if not os.path.exists('output/flipbook.html'):
                logger.error("flipbook.html not found")
                return "Flipbook not generated yet", 500
            return send_from_directory('output', 'flipbook.html')
        
        # Try serving from output directory first
        if os.path.exists(os.path.join('output', path)):
            return send_from_directory('output', path)
        
        # Then try turnjs directory
        if os.path.exists(os.path.join('turnjs', path)):
            return send_from_directory('turnjs', path)
        
        # If file not found
        logger.error(f"File not found: {path}")
        return f"File {path} not found", 404
        
    except Exception as e:
        logger.error(f"Error serving {path}: {str(e)}")
        return "Server error", 500

@app.before_request
def before_request():
    if not request.is_secure and app.env != 'development':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return "File not found", 404

@app.errorhandler(500)
def internal_error(error):
    return "Internal server error", 500

if __name__ == '__main__':
    # Only for development
    app.config['SERVER_NAME'] = None  # Don't restrict hostname in development
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting development server on port {port}")
    app.run(host='0.0.0.0', port=port) 