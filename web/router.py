from http import HTTPStatus

from webob import Request, Response
from webob.exc import HTTPNotFound


class Router:
    def __init__(self):
        self.routes = {}
        self.not_found_handler = None

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
        response = Response()

        handler = self.routes.get(request.path_info)
        if handler:
            try:
                handler(request, response)
            except Exception as err:
                response.status = HTTPStatus.INTERNAL_SERVER_ERROR
                response.json = {'error': f'internal server error: {err}'}
        else:
            if self.not_found_handler:
                self.not_found_handler(request, response)
            else:
                response = HTTPNotFound()

        return response(environ, start_response)
