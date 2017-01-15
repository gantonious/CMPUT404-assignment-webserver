from httpresponse import HttpResponse

class OK(HttpResponse):
    def __init__(self):
        HttpResponse.__init__(self, 200, "OK")

class NotFound(HttpResponse):
    def __init__(self):
        HttpResponse.__init__(self, 404, "Not Found")

class MethodNotAllowed(HttpResponse):
    def __init__(self):
        HttpResponse.__init__(self, 405, "Method Not Allowed")