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