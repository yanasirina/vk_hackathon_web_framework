from webob import Request
from webob.exc import HTTPNotFound, HTTPInternalServerError
from typing import Callable, Optional, Dict


class Router:
    routes: Dict[str, Callable]
    not_found_handler: Optional[Callable]

    def __init__(self) -> None:
        self.routes = {}
        self.not_found_handler = None

    def route(self, path: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.routes[path] = func
            return func

        return decorator

    def not_found(self, func: Callable) -> Callable:
        self.not_found_handler = func
        return func

    def __call__(self, environ: Dict[str, str], start_response: Callable) -> Callable:
        request = Request(environ)
        response = None

        handler = self.routes.get(request.path_info)
        if handler:
            try:
                response = handler(request)
            except Exception:
                response = HTTPInternalServerError()
        else:
            if self.not_found_handler:
                response = self.not_found_handler(request)
            else:
                response = HTTPNotFound()

        return response(environ, start_response)
