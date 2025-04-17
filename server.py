import http.server
import socketserver
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', 10000))
DIRECTORY = "output"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        logger.info("%s - - [%s] %s" % (self.address_string(), self.log_date_time_string(), format%args))

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    logger.info(f"Serving at http://0.0.0.0:{PORT}")
    httpd.serve_forever() 