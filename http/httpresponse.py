# Copyright 2016 George Antonious
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