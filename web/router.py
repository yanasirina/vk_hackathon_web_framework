from http import HTTPMethod

from webob import Request, Response
from webob.exc import HTTPNotFound, HTTPInternalServerError, HTTPBadRequest
from parse import parse
from .middleware import Middleware


class Router:
    def __init__(self):
        self.routes = {}
        self.not_found_handler = None

    def _add_route(self, method, path, func, middlewares: list[Middleware] | None = None):
        if middlewares is None:
            middlewares = []

        if path not in self.routes:
            self.routes[path] = {}

        self.routes[path][method] = self._apply_middlewares(func, middlewares)

    def get(self, path, middlewares: list[Middleware] | None = None):
        def decorator(func):
            self._add_route(HTTPMethod.GET, path, func, middlewares)
            return func

        return decorator

    def post(self, path, middlewares: list[Middleware] | None = None):
        def decorator(func):
            self._add_route(HTTPMethod.POST, path, func, middlewares)
            return func

        return decorator

    def put(self, path, middlewares: list[Middleware] | None = None):
        def decorator(func):
            self._add_route(HTTPMethod.PUT, path, func, middlewares)
            return func

        return decorator

    def patch(self, path, middlewares: list[Middleware] | None = None):
        def decorator(func):
            self._add_route(HTTPMethod.PATCH, path, func, middlewares)
            return func

        return decorator

    def delete(self, path, middlewares: list[Middleware] | None = None):
        def decorator(func):
            self._add_route(HTTPMethod.DELETE, path, func, middlewares)
            return func

        return decorator

    def not_found(self, func):
        self.not_found_handler = func
        return func

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = Response()

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
            if self.not_found_handler:
                self.not_found_handler(request)
            else:
                response = HTTPNotFound()

        return response(environ, start_response)

    @staticmethod
    def _apply_middlewares(handler, middlewares):
        for middleware in reversed(middlewares):
            handler = middleware(handler)

        return handler

    
    def _find_handler(self, request):
        for route, method_handlers in self.routes.items():
            parse_result = parse(route, request.path)
            if parse_result:
                handler = method_handlers.get(request.method)
                if handler:
                    return handler, parse_result.named
        return None, None
