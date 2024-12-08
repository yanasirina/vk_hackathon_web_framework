from http import HTTPMethod
from typing import Type

from webob import Request, Response
from webob.exc import HTTPNotFound, HTTPInternalServerError

from .middleware import Middleware


class Router:
    def __init__(self):
        self.routes = {}
        self.not_found_handler = None
        self.global_middlewares: list[Type[Middleware]] = []

    def use_middleware(self, middleware: Type[Middleware]):
        self.global_middlewares.append(middleware)

    def _add_route(self, method, path, func, middlewares: list[Type[Middleware]] | None = None):
        if middlewares is None:
            middlewares = []

        if path not in self.routes:
            self.routes[path] = {}

        self.routes[path][method] = self._apply_middlewares(
            func,
            self.global_middlewares + middlewares,
        )

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

        method_routes = self.routes.get(request.path_info, {})
        handler = method_routes.get(request.method)

        if handler is not None:
            try:
                response = handler(request)
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
