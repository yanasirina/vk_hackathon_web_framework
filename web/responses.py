from webob import Response as _Response
from typing import Any


class Response(_Response):
    """
    Inherit your responses from this class
    """


class JsonResponse(Response):
    def __init__(self, body: dict, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, json_body=body, **kwargs)
        self.content_type = 'application/json'
