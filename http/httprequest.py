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