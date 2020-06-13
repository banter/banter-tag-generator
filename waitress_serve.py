from app import app
from waitress import serve
import os

if __name__ == "__main__":
    hostname = os.popen('hostname').read()
    if 'Austin' not in hostname:
        port = 5000
    else:
        port = 5005
    host = '0.0.0.0'
    serve(app, host=host, port=port)
    print(f"Application Listeing on: {host}:{port}")