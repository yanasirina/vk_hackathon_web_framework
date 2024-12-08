from webob import Response as _Response


class Response(_Response):
    """
    Inherit your responses from this class
    """


class JsonResponse(Response):
    def __init__(self, body: dict, *args, **kwargs):
        super().__init__(*args, json_body=body, **kwargs)
        self.content_type = 'application/json'
