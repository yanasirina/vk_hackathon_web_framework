import datetime
import logging

from config import get_config

import web
import web.responses


router = web.Router()
logger = logging.getLogger('app')


class ExampleMiddleware(web.Middleware):
    def before(self, request):
        logger.info('before middleware call')

    def after(self, _request, response):
        logger.info('after middleware call')
        return response


@router.get('/main')
def html_example(_request):
    response = web.responses.HTMLResponse(
        template_path='templates/index.html',
        context={'today_date': datetime.date.today()}
    )
    return response


@router.get('/hello', middlewares=[ExampleMiddleware])
def get_example(request):
    logger.info(f'got {request=}')
    return web.responses.JsonResponse({'message': 'hello, world!'})


@router.get('/hello/{name}/{age}')
def get_example_with_params(request, name: str, age: int):
    logger.info(f'got {request=}')
    return web.responses.JsonResponse({'message': 'hello, world!', 'name': name, 'age': age})


@router.post('/hello', middlewares=[ExampleMiddleware])
def post_example(request):
    logger.info(f'got {request=}')
    return web.responses.JsonResponse({'message': 'hello, world!', 'data': request.json})


@router.not_found
def custom_404(_request):
    return web.responses.JsonResponse({'error': 'route not found'})


def main() -> None:
    config = get_config()
    web.Server(router, config).run()


if __name__ == '__main__':
    main()
