from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def serve_flipbook():
    return send_from_directory('output', 'flipbook.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('output', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000))) 