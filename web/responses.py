from enum import Enum

from webob import Response as _Response
from typing import Any
from jinja2 import Environment, FileSystemLoader


class ContentType(Enum):
    JSON = "application/json"
    HTML = "text/html"


class Response(_Response):
    """
    Inherit your responses from this class
    """


class JsonResponse(Response):
    def __init__(self, body: dict, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, json_body=body, content_type=ContentType.JSON.value, **kwargs)


class HTMLResponse(Response):
    def __init__(self, template_path: str, context: dict, *args: Any, templates_dir: str = '', **kwargs: Any) -> None:
        env = Environment(loader=FileSystemLoader(templates_dir))
        template = env.get_template(template_path)
        rendered_html = template.render(context)
        super().__init__(*args, body=rendered_html, content_type=ContentType.HTML.value, **kwargs)

