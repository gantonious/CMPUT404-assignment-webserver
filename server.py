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

import os.path
import shlex
import mimetypes
import SocketServer

class HttpRequest:
    def __init__(self, method, path):
        self._method = method
        self._path = path
        self._headers = {}
        self._body = ""

    def with_header(self, key, value):
        self._headers[key] = value
        return self
    
    def with_body(self, body):
        self._body = body
        return self

    def method(self):
        return self._method

    def path(self):
        return self._path

    def headers(self):
        return self._headers
    
    def header(self, key):
        if key in self.headers():
            return self.headers()[key]
        return None
    
    def body(self):
        return self._body

    def has_body(self):
        return not len(self._body)

class HttpRequestParser:
    def parse(self, serailized_request):
        state = 0
        request = None
        body = ""

        for line in serailized_request.split("\n"):
            if state == 0:
                request = self._parse_request_line(line)
                state = 1
            elif state == 1:
                if line.strip() == "":
                    state = 2
                else:
                    self._parse_header_line(line, request)
            elif state == 2:
                if line != "\n":
                    body += line
        
        request.with_body(body)
        return request
                
    def _parse_request_line(self, request_line):
        request_tokens = shlex.split(request_line)
        return HttpRequest(request_tokens[0], request_tokens[1])
    
    def _parse_header_line(self, header_line, request):
        header_tokens = header_line.split(":")
        request.with_header(header_tokens[0].strip(), header_tokens[1].strip())

class HttpResponse:
    def __init__(self, response_code, response_message):
        self._response_code = response_code
        self._response_message = response_message
        self._headers = {}
        self._body = ""

    def with_header(self, key, value):
        self._headers[key] = value
        return self
    
    def with_body(self, body):
        self._body = body
        return self

    def response_code(self):
        return self._response_code

    def response_message(self):
        return self._response_message

    def serialize(self):
        return self._build_response_line() + \
               self._build_header_lines() + \
               self._build_body_line()

    def _build_response_line(self):
        return "HTTP/1.1 {0} {1}".format(self._response_code, self._response_message)
    
    def _build_header_lines(self):
        header_lines = ["{0}: {1}".format(k, v) for k, v in self._headers.iteritems()]

        if header_lines:
            return "\r\n" + "\r\n".join(header_lines)
        return ""

    def _build_body_line(self):
        if self._body:
            return "\r\n\r\n{0}\r\n".format(self._body)
        return "\r\n\r\n"

class OK(HttpResponse):
    def __init__(self):
        HttpResponse.__init__(self, 200, "OK")

class NotFound(HttpResponse):
    def __init__(self):
        HttpResponse.__init__(self, 404, "Not Found")

class MethodNotAllowed(HttpResponse):
    def __init__(self):
        HttpResponse.__init__(self, 405, "Method Not Allowed")

class HttpRequestHandler:
    def can_handle(self, http_request):
        return False

    def handle(self, http_request):
        return None

class UnimplementedRequestHandler(HttpRequestHandler):
    def can_handle(self, http_request):
        return True

    def handle(self, http_request):
        return MethodNotAllowed()

def load_file_as_string(path):
    with open(path, 'r') as file:
        return file.read()

def get_mime_type_for_path(path):
    guessed_type = mimetypes.guess_type(path)[0]
    return guessed_type or "text/plain"

def handle_file_request(path):
    try:
        return OK().with_header("Content-Type", get_mime_type_for_path(path)) \
                   .with_body(load_file_as_string(path))
    except:
        return NotFound()

class BadPathRequestHandler(HttpRequestHandler):
    def can_handle(self, http_request):
        www_absolute_path= os.path.abspath("./www")
        request_absolute_path = os.path.abspath("./www" + http_request.path())
        return not request_absolute_path.startswith(www_absolute_path)

    def handle(self, http_request):
        return NotFound()

class DirectoryRequestHandler(HttpRequestHandler):
    def can_handle(self, http_request):
        return http_request.method() == "GET" and \
               http_request.path().endswith("/")
    
    def handle(self, http_request):
        path = "www" + http_request.path() + "index.html"
        return handle_file_request(path)

class FileRequestHandler(HttpRequestHandler):
    def can_handle(self, http_request):
        return http_request.method() == "GET"

    def handle(self, http_request):
        path = "www" + http_request.path()
        return handle_file_request(path)

class WebServer(SocketServer.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, http_request_parser):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self._http_request_parser = http_request_parser
        self._request_handlers = []
        
    def register_request_handler(self, request_handler):
        self._request_handlers.append(request_handler)
    
    def http_request_parser(self):
        return self._http_request_parser

    def request_handlers(self):
        return self._request_handlers

class WebRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        raw_http_request = self.request.recv(1024).strip()
        http_request = self._parse_request(raw_http_request)
        request_handler = self._get_request_handler_for(http_request)

        http_response = request_handler.handle(http_request)
        raw_http_response = http_response.serialize()

        self.request.sendall(raw_http_response)

    def _parse_request(self, raw_http_request):
        return self.server.http_request_parser().parse(raw_http_request)
    
    def _get_request_handler_for(self, request):             
        for handler in self.server.request_handlers():
            if (handler.can_handle(request)):
                return handler
        return UnimplementedRequestHandler()

def build_web_server(host, port):
    http_request_parser = HttpRequestParser()
    
    WebServer.allow_reuse_address = True
    server = WebServer((host, port), WebRequestHandler, http_request_parser)

    server.register_request_handler(BadPathRequestHandler())
    server.register_request_handler(DirectoryRequestHandler())
    server.register_request_handler(FileRequestHandler())
    
    return server

if __name__ == "__main__":
    server = build_web_server("localhost", 8080)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()