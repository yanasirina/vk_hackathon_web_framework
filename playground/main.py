import os

import web
from web import JsonResponse

import logging

app = web.Router()

logger = logging.getLogger('app')


@app.route('/hello')
def json_example(_request):
    response = JsonResponse({'message': 'hello, world!'})
    return response


@app.not_found
def custom_404(_request):
    response = JsonResponse({'error': 'route not found'})
    return response


def main() -> None:
    config = {
        'bind': '0.0.0.0:8080',
        'workers': os.cpu_count(),
        'loglevel': 'debug',
    }

    web.Server(app, config).run()


if __name__ == '__main__':
    main()
