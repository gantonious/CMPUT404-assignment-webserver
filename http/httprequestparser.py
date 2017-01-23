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

import shlex
from http.httprequest import HttpRequest

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