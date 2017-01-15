import os.path
from webserver.httprequesthandler import HttpRequestHandler
from http.httpresponsetypes import *

def load_file_as_string(path):
    with open(path, 'r') as file:
        return file.read()

def handle_file_request(path, file_type):
    try:
        return OK().with_header("Content-Type", file_type) \
                    .with_body(load_file_as_string(path))
    except:
        return NotFound()

class BadPathRequestHandler(HttpRequestHandler):
    def can_handle(self, http_request):
        real_path = os.path.realpath("./www" + http_request.path())
        return "www" not in real_path

    def handle(self, http_request):
        return NotFound()

class DirectoryRequestHandler(HttpRequestHandler):
    def can_handle(self, http_request):
        return http_request.method() == "GET" and \
               http_request.path().endswith("/")
    
    def handle(self, http_request):
        path = "www" + http_request.path() + "index.html"
        return handle_file_request(path, "text/html")

class FileRequestHandler(HttpRequestHandler):
    def __init__(self):
        self._files = {}

    def register_mime_type(self, file_extension, mime_type):
        self._files[file_extension] = mime_type

    def get_mime_type_for_path(self, path):
        file_types = [v for k, v in self._files.iteritems() if path.endswith(k)]
        return file_types[0] if file_types else "text/plain"

    def can_handle(self, http_request):
        return http_request.method() == "GET"

    def handle(self, http_request):
        path = "www" + http_request.path()
        return handle_file_request(path, self.get_mime_type_for_path(path))