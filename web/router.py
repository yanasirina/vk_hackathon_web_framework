import sys
from typing import List, Optional

from webob import Request, Response
from webob.exc import HTTPNotFound, HTTPInternalServerError

from .middleware import Middleware


class Router:
    def __init__(self):
        self.routes = {}
        self.not_found_handler = None

    def route(self, path, middlewares: Optional[List[Middleware]] = None):
        if middlewares is None:
            middlewares = []

        def decorator(func):
            self.routes[path] = self._apply_middlewares(func, middlewares)
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
                response = handler(request)
            except Exception as err:
                print(err, file=sys.stdout)
                response = HTTPInternalServerError()
        else:
            if self.not_found_handler:
                self.not_found_handler(request, response)
            else:
                response = HTTPNotFound()

        return response(environ, start_response)

    @staticmethod
    def _apply_middlewares(handler, middlewares):
        for middleware in reversed(middlewares):
            handler = middleware(handler)

        return handler
