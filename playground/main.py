import os

from webob import Response

import web
from web.router import logger

router = web.Router()


@router.get('/hello')
def get_example(request):
    logger.info(f'got {request=}')
    return Response(content_type='application/json', json={'message': 'hello, world!'})



@router.post('/hello')
def post_example(request):
    logger.info(f'got {request=}')
    return Response(content_type='application/json', json={'message': 'hello, world!', 'data': request.data})


@router.not_found
def custom_404(request):
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

    web.Server(router, config).run()


if __name__ == '__main__':
    main()
