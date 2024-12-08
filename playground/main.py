import os

import logging

import web
from web import JsonResponse

router = web.Router()
logger = logging.getLogger('app')


@router.get('/hello')
def get_example(request):
    logger.info(f'got {request=}')
    return JsonResponse({'message': 'hello, world!'})


@router.post('/hello')
def post_example(request):
    logger.info(f'got {request=}')
    return JsonResponse({'message': 'hello, world!', 'data': request.json})


@router.not_found
def custom_404(_request):
    return JsonResponse({'error': 'route not found'})


def main() -> None:
    config = {
        'bind': '0.0.0.0:8080',
        'workers': os.cpu_count(),
        'loglevel': 'info',
    }

    web.Server(router, config).run()


if __name__ == '__main__':
    main()
