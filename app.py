import os
import sys
import logging
from flask import Flask, send_from_directory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

try:
    app = Flask(__name__, static_folder='output')
    logger.info("Flask application initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Flask: {str(e)}")
    sys.exit(1)

@app.route('/')
def serve_flipbook():
    try:
        logger.info("Serving flipbook.html")
        return send_from_directory('output', 'flipbook.html')
    except Exception as e:
        logger.error(f"Error serving flipbook.html: {str(e)}")
        return "Error serving flipbook", 500

@app.route('/<path:path>')
def serve_static(path):
    try:
        logger.info(f"Serving static file: {path}")
        return send_from_directory('output', path)
    except Exception as e:
        logger.error(f"Error serving static file {path}: {str(e)}")
        return "Error serving file", 500

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 10000))
        logger.info(f"Starting server on port {port}")
        # Use 0.0.0.0 to bind to all available network interfaces
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        sys.exit(1) 