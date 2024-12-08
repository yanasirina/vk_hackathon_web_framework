from webob import Request, Response
from webob.exc import HTTPNotFound, HTTPInternalServerError
from http import HTTPMethod


class Router:
    def __init__(self):
        self.routes = {}
        self.not_found_handler = HTTPNotFound

    def add_route(self, method, path, func):
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method] = func

    def get(self, path):
        def decorator(func):
            self.add_route(HTTPMethod.GET, path, func)
            return func

        return decorator

    def post(self, path):
        def decorator(func):
            self.add_route(HTTPMethod.POST, path, func)
            return func

        return decorator

    def put(self, path):
        def decorator(func):
            self.add_route(HTTPMethod.PUT, path, func)
            return func

        return decorator

    def patch(self, path):
        def decorator(func):
            self.add_route(HTTPMethod.PATCH, path, func)
            return func

        return decorator

    def delete(self, path):
        def decorator(func):
            self.add_route(HTTPMethod.DELETE, path, func)
            return func

        return decorator

    def not_found(self, func):
        self.not_found_handler = func
        return func

    def __call__(self, environ, start_response) -> Response:
        request = Request(environ)

        method_routes = self.routes.get(request.path_info, {})
        handler = method_routes.get(request.method)

        if handler is not None:
            try:
                response = handler(request)
            except Exception:
                response = HTTPInternalServerError()
        else:
            response = self.not_found_handler(request)

        return response(environ, start_response)
