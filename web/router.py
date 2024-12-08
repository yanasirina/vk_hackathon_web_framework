import sys

from webob import Request
from webob.exc import HTTPNotFound, HTTPInternalServerError
from http import HTTPMethod
import logging

logger = logging.getLogger(__name__)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_formatter = logging.Formatter("STDOUT: %(levelname)s - %(message)s")
stdout_handler.setFormatter(stdout_formatter)
logger.addHandler(stdout_handler)


class Router:
    def __init__(self):
        self.routes = {}
        self.not_found_handler = None

    def add_route(self, method, path, func):
        logger.info(f'add route, {method}, {path}, {func}')
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method] = func


    def get(self, path):
        logger.info(f'get route, {path}')
        def decorator(func):
            self.add_route(HTTPMethod.GET, path, func)
            return func

        return decorator

    def post(self, path):
        logger.info(f'post route, {path}')
        def decorator(func):
            self.add_route(HTTPMethod.POST, path, func)
            return func

        return decorator

    def put(self, path):
        logger.info(f'put route, {path}')
        def decorator(func):
            self.add_route(HTTPMethod.PUT, path, func)
            return func

        return decorator

    def delete(self, path):
        logger.info(f'delete route, {path}')
        def decorator(func):
            self.add_route(HTTPMethod.DELETE, path, func)
            return func

        return decorator

    def not_found(self, func):
        self.not_found_handler = func
        return func

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = None

        method_routes = self.routes.get(request.path_info, {})
        handler = method_routes.get(request.method)

        if handler is not None:
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
