from webob import Request
from webob.exc import HTTPNotFound, HTTPInternalServerError
from parse import parse


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
        response = None

        handler, kwargs = self._find_handler(request.path)

        if kwargs and handler:
            # получаем типы аргументов из сигнатуры функции
            signature = handler.__annotations__
            # приводим аргументы к нужным типам
            try:
                kwargs = {name: signature[name](value) for name, value in kwargs.items()}
            except ValueError:
                ...


        if handler:
            try:
                response = handler(request, **kwargs)
            except Exception:
                response = HTTPInternalServerError()
        else:
            if self.not_found_handler:
                response = self.not_found_handler(request)
            else:
                response = HTTPNotFound()

        return response(environ, start_response)


    def _find_handler(self, path):
        for route, handler in self.routes.items():
            parse_result = parse(route, path)
            if parse_result:
                return handler, parse_result.named
        return None, None
