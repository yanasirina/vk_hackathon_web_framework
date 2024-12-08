from webob import Request
from webob.exc import HTTPNotFound, HTTPInternalServerError


class Router:
    def __init__(self):
        self.routes = {}
        self.not_found_handler = HTTPNotFound

    def route(self, path):
        def decorator(func):
            self.routes[path] = func
            return func

        return decorator

    def not_found(self, func):
        self.not_found_handler = func
        return func

    def __call__(self, environ, start_response):
        request = Request(environ)

        handler = self.routes.get(request.path_info)
        if handler:
            try:
                response = handler(request)
            except Exception:
                response = HTTPInternalServerError()
        else:
            response = self.not_found_handler(request)

        return response(environ, start_response)
