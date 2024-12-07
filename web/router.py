class Router:
    def __init__(self):
        self.routes = {}

    def route(self, path):
        def decorator(func):
            self.routes[path] = func
            return func

        return decorator

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "/")
        handler = self.routes.get(path)
        if handler:
            status = "200 OK"
            response_headers = [("Content-Type", "text/plain")]
            start_response(status, response_headers)
            return [handler(environ).encode("utf-8")]
        else:
            status = "404 Not Found"
            response_headers = [("Content-Type", "text/plain")]
            start_response(status, response_headers)
            return [b"Not Found"]