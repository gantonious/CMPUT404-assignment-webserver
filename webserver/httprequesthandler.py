from http.httpresponsetypes import MethodNotAllowed

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