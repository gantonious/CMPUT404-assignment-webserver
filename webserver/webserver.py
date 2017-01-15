import SocketServer
from httprequesthandler import UnimplementedRequestHandler

class WebServer(SocketServer.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, http_request_parser):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self._http_request_parser = http_request_parser
        self._request_handlers = []
        
    def register_request_handler(self, request_handler):
        self._request_handlers = self._request_handlers.append(request_handler)
    
    def http_request_parser(self):
        return self._http_request_parser

    def request_handlers(self):
        return self._request_handlers

class WebRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        raw_http_request = self.request.recv(1024).strip()
        http_request = self._parse_request(raw_http_request)
        request_handler = self._get_request_handler_for(http_request)
        
        http_response = request_handler.handle(http_request)
        raw_http_response = http_response.serialize()

        self.request.sendall(raw_http_response)

    def _parse_request(self, raw_http_request):
        return self.server.http_request_parser()
    
    def _get_request_handler_for(self, request):             
        for handler in self.server.request_handlers():
            if (handler.can_handle(request)):
                return handler
        return UnimplementedRequestHandler()