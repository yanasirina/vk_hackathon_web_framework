import os
import datetime
import logging

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
def get_example(request):
    logger.info(f'got {request=}')
    return web.responses.JsonResponse({'message': 'hello, world!'})


class ExampleMiddleware(web.Middleware):
    def before(self, request):
        print('before middleware call')

    def after(self, request, response):
        print('after middleware call')
        return response


@router.post('/hello', middlewares=[ExampleMiddleware])
def post_example(request):
    logger.info(f'got {request=}')
    return web.responses.JsonResponse({'message': 'hello, world!', 'data': request.json})


@router.not_found
def custom_404(_request):
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
