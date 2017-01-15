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