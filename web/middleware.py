from webob import Request, Response


class Middleware:
    def __init__(self, handler) -> None:
        self.handler = handler

    def before(self, request: Request) -> None:
        pass

    def after(self, _request: Request, response: Response) -> Response:
        return response

    def __call__(self, request: Request) -> Response:
        self.before(request)
        response = self.handler(request)
        return self.after(request, response)
