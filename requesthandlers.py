# Copyright 2017 George Antonious
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