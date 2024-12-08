from http import HTTPMethod

from webob import Request, Response
from webob.exc import HTTPNotFound, HTTPInternalServerError, HTTPBadRequest
from parse import parse


import logging
mylog = logging.getLogger('app')
mylog.setLevel(logging.DEBUG)

class Router:
    def __init__(self):
        self.routes = {}
        self.not_found_handler = HTTPNotFound

    def _add_route(self, method, path, func):
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method] = func

    def get(self, path):
        def decorator(func):
            self._add_route(HTTPMethod.GET, path, func)
            return func

        return decorator

    def post(self, path):
        def decorator(func):
            self._add_route(HTTPMethod.POST, path, func)
            return func

        return decorator

    def put(self, path):
        def decorator(func):
            self._add_route(HTTPMethod.PUT, path, func)
            return func

        return decorator

    def patch(self, path):
        def decorator(func):
            self._add_route(HTTPMethod.PATCH, path, func)
            return func

        return decorator

    def delete(self, path):
        def decorator(func):
            self._add_route(HTTPMethod.DELETE, path, func)
            return func

        return decorator

    def not_found(self, func):
        self.not_found_handler = func
        return func

    def __call__(self, environ, start_response) -> Response:
        request = Request(environ)

        # method_routes = self.routes.get(request.path_info, {})
        # handler = method_routes.get(request.method)

        handler, kwargs = self._find_handler(request)

        if kwargs and handler:
            # получаем типы аргументов из сигнатуры функции
            signature = handler.__annotations__
            # приводим аргументы к нужным типам
            try:
                kwargs = {name: signature[name](value) for name, value in
                          kwargs.items()}
            except ValueError:
                response = HTTPBadRequest(
                    json={"error": "invalid type arguments"})
                return response(environ, start_response)

        if handler is not None:
            try:

                response = handler(request, **kwargs)
            except Exception:
                response = HTTPInternalServerError()
        else:
            response = self.not_found_handler(request)

        return response(environ, start_response)

    def _find_handler(self, request):
        for route in self.routes:
            parse_result = parse(route, request.path)
            mylog.info(f'{parse_result=}')
            if parse_result:
                handler = self.routes[route].get(request.method)
                return handler, parse_result.named
        return None, None
