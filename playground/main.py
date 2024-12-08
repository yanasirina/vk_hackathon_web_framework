import os
import datetime
import logging

from webob import Request
from web.responses import JsonResponse

import web
import web.responses


router = web.Router()
logger = logging.getLogger('app')


@router.get('/main')
def html_example(_request):
    response = web.responses.HTMLResponse(
        template_path='templates/index.html',
        context={'today_date': datetime.date.today()}
    )
    return response


@router.get('/hello')
def get_example(request: Request) -> JsonResponse:
    logger.info(f'got {request=}')
    return web.responses.JsonResponse({'message': 'hello, world!'})


@router.post('/hello')
def post_example(request: Request) -> JsonResponse:
    logger.info(f'got {request=}')
    return web.responses.JsonResponse({'message': 'hello, world!', 'data': request.json})


@router.not_found
def custom_404(_request: Request) -> JsonResponse:
    return web.responses.JsonResponse({'error': 'route not found'})


def main() -> None:
    config = {
        'bind': '0.0.0.0:8080',
        'workers': os.cpu_count(),
        'loglevel': 'info',
    }

    web.Server(router, config).run()


if __name__ == '__main__':
    main()
