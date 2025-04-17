from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', 10000))
DIRECTORY = "output"

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Always serve flipbook.html for root path
        if self.path == '/':
            self.path = '/flipbook.html'
        return super().do_GET()

    def log_message(self, format, *args):
        logger.info("%s - - [%s] %s" % (self.address_string(), self.log_date_time_string(), format%args))

def run(server_class=HTTPServer, handler_class=Handler):
    server_address = ('0.0.0.0', PORT)
    httpd = server_class(server_address, handler_class)
    logger.info(f"Starting server at http://0.0.0.0:{PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    run() 