import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


import string
from modules import request_follow, request_history, request_relations, reduce_data
from modules.config_parser import data_path
from modules.console_log import INFO, PROC, WARN


def check_and_run(file_name: string, func):
    PROC(f"Checking for file {file_name}")
    if not os.path.exists(f"{data_path}{file_name}"):
        WARN(f"{file_name} not found, getting data...")
        func()
    else:
        INFO(f"Found {file_name}.")

check_and_run("follow.json", request_follow)
check_and_run("bilibili_history.json", request_history)
PROC("Parsing interaction data...")
request_relations()

check_and_run("main_data.json", reduce_data)

INFO("Finished handling data.")

import threading
import sys
import time
import http.server
import os

PORT = 8080
DIRECTORY = "../dist"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = super().translate_path(path)
        return os.path.join(DIRECTORY, os.path.relpath(path, self.directory))

def run_server():
    server = http.server.HTTPServer(('', PORT), CustomHTTPRequestHandler)
    print(f"Serving HTTP on http://localhost:{PORT}")
    server.serve_forever()

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Server stopped by user.")
    sys.exit(0)

