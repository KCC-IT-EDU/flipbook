from flask import Flask, send_from_directory, send_file
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
app.config['ENV'] = 'production'
app.config['DEBUG'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

# Ensure the output directory exists
if not os.path.exists('output'):
    os.makedirs('output')

@app.route('/')
def serve_flipbook():
    try:
        logger.info("Serving flipbook.html")
        if not os.path.exists('output/flipbook.html'):
            logger.error("flipbook.html not found in output directory")
            return "Flipbook not generated yet. Please run main.py first.", 500
        return send_from_directory('output', 'flipbook.html')
    except Exception as e:
        logger.error(f"Error serving flipbook.html: {str(e)}")
        return "Error serving flipbook", 500

@app.route('/output/<path:filename>')
def serve_output(filename):
    try:
        logger.info(f"Serving output file: {filename}")
        file_path = os.path.join('output', filename)
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return f"File {filename} not found", 404
        return send_from_directory('output', filename)
    except Exception as e:
        logger.error(f"Error serving output file {filename}: {str(e)}")
        return f"Error serving {filename}", 500

@app.route('/turnjs/<path:filename>')
def serve_turnjs(filename):
    try:
        logger.info(f"Serving turnjs file: {filename}")
        file_path = os.path.join('turnjs', filename)
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return f"File {filename} not found", 404
        return send_from_directory('turnjs', filename)
    except Exception as e:
        logger.error(f"Error serving turnjs file {filename}: {str(e)}")
        return f"Error serving {filename}", 500

@app.route('/<path:path>')
def serve_static(path):
    try:
        logger.info(f"Serving static file: {path}")
        # Check if file exists in output directory
        output_path = os.path.join('output', path)
        if os.path.exists(output_path):
            return send_from_directory('output', path)
        
        # If not in output, try turnjs directory
        turnjs_path = os.path.join('turnjs', path)
        if os.path.exists(turnjs_path):
            return send_from_directory('turnjs', path)
        
        # If file not found in either directory
        logger.error(f"File not found: {path}")
        return "File not found", 404
            
    except Exception as e:
        logger.error(f"Error serving static file {path}: {str(e)}")
        return "Error serving file", 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return "File not found", 404

@app.errorhandler(500)
def internal_error(error):
    return "Internal server error", 500

if __name__ == '__main__':
    # Only for development
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting development server on port {port}")
    app.run(host='0.0.0.0', port=port) 