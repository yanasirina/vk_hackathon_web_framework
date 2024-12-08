from abc import ABC, abstractmethod

from webob import Request, Response


class Middleware(ABC):
    def __init__(self, handler) -> None:
        self.handler = handler

    @abstractmethod
    def before(self, request: Request) -> None:
        pass

    @abstractmethod
    def after(self, request: Request, response: Response) -> Response:
        pass

    def __call__(self, request: Request) -> Response:
        self.before(request)
        response = self.handler(request)
        return self.after(request, response)
