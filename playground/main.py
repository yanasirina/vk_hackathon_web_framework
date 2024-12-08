import os

from webob import Response
from webob import Request

import web


app = web.Router()


@app.route('/hello')
def json_example(request: Request) -> Response:
    _ = request.method
    response = Response()
    response.content_type = 'application/json'
    response.json = {'message': 'hello, world!'}
    return response


@app.not_found
def custom_404(request: Request) -> Response:
    _ = request.method
    response = Response()
    response.content_type = 'application/json'
    response.json = {'error': 'route not found'}
    return response


def main() -> None:
    config = {
        'bind': '0.0.0.0:8080',
        'workers': os.cpu_count(),
        'loglevel': 'info',
    }

    web.Server(app, config).run()


if __name__ == '__main__':
    main()
