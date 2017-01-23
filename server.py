#  coding: utf-8 

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, George Antonious
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

import SocketServer
from webserver.webserver import WebServer
from webserver.webserver import WebRequestHandler
from http.httprequestparser import HttpRequestParser
from requesthandlers import *

def build_file_request_handler():
    file_request_handler = FileRequestHandler()
    file_request_handler.register_mime_type("html", "text/html")
    file_request_handler.register_mime_type("css", "text/css")
    file_request_handler.register_mime_type("png", "image/png")

    return file_request_handler

def build_web_server(host, port):
    http_request_parser = HttpRequestParser()
    
    WebServer.allow_reuse_address = True
    server = WebServer((host, port), WebRequestHandler, http_request_parser)

    server.register_request_handler(BadPathRequestHandler())
    server.register_request_handler(DirectoryRequestHandler())
    server.register_request_handler(build_file_request_handler())
    
    return server

if __name__ == "__main__":
    server = build_web_server("localhost", 8080)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
