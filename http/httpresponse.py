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