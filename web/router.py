from http import HTTPMethod

from webob import Request, Response
from webob.exc import HTTPNotFound, HTTPInternalServerError
from typing import Callable, Optional, Dict

from .middleware import Middleware


class Router:
    routes: Dict[str, Dict[str, Callable]]
    not_found_handler: Optional[Callable]

    def __init__(self) -> None:
        self.routes = {}
        self.not_found_handler = None

    def _add_route(
            self,
            method: str,
            path: str,
            func: Callable,
            middlewares: list[Middleware] | None = None
    ) -> None:
        if middlewares is None:
            middlewares = []

        if path not in self.routes:
            self.routes[path] = {}

        self.routes[path][method] = self._apply_middlewares(func, middlewares)

    def get(
            self,
            path: str,
            middlewares: list[Middleware] | None = None
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            self._add_route(HTTPMethod.GET, path, func, middlewares)
            return func

        return decorator

    def post(
            self,
            path: str,
            middlewares: list[Middleware] | None = None
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            self._add_route(HTTPMethod.POST, path, func, middlewares)
            return func

        return decorator

    def put(
            self,
            path: str,
            middlewares: list[Middleware] | None = None
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            self._add_route(HTTPMethod.PUT, path, func, middlewares)
            return func

        return decorator

    def patch(
            self,
            path: str,
            middlewares: list[Middleware] | None = None
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            self._add_route(HTTPMethod.PATCH, path, func, middlewares)
            return func

        return decorator

    def delete(
            self,
            path: str,
            middlewares: list[Middleware] | None = None
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            self._add_route(HTTPMethod.DELETE, path, func, middlewares)
            return func

        return decorator

    def not_found(self, func: Callable) -> Callable:
        self.not_found_handler = func
        return func

    def __call__(self, environ: Dict[str, str], start_response: Callable) -> Response:

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
    def _apply_middlewares(handler, middlewares: list[Middleware]) -> Callable:
        for middleware in reversed(middlewares):
            handler = middleware(handler)

        return handler
