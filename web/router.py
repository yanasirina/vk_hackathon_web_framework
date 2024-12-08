from http import HTTPMethod

from webob import Request, Response
from webob.exc import HTTPNotFound, HTTPInternalServerError
from typing import Callable, Optional, Dict


class Router:
    routes: Dict[str, Dict[str, Callable]]
    not_found_handler: Optional[Callable]

    def __init__(self) -> None:
        self.routes = {}
        self.not_found_handler = HTTPNotFound

    def add_route(self, method: str, path: str, func: Callable) -> None:
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method] = func

    def get(self, path: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.add_route(HTTPMethod.GET, path, func)
            return func

        return decorator

    def post(self, path: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.add_route(HTTPMethod.POST, path, func)
            return func

        return decorator

    def put(self, path: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.add_route(HTTPMethod.PUT, path, func)
            return func

        return decorator

    def patch(self, path: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.add_route(HTTPMethod.PATCH, path, func)
            return func

        return decorator

    def delete(self, path: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.add_route(HTTPMethod.DELETE, path, func)
            return func

        return decorator

    def not_found(self, func: Callable) -> Callable:
        self.not_found_handler = func
        return func

    def __call__(self, environ: Dict[str, str], start_response: Callable) -> Response:
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
