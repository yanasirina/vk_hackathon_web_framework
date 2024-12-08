import os

import web
from web import JsonResponse


app = web.Router()


class ExampleMiddleware(web.Middleware):
    def before(self, request):
        print('before middleware call')

    def after(self, request, response):
        print('after middleware call')
        return response


@app.route('/hello', middlewares=[ExampleMiddleware])
def json_example(_request):
    response = JsonResponse({'message': 'hello, world!'})
    print('handler')
    return response


@app.not_found
def custom_404(_request):
    response = JsonResponse({'error': 'route not found'})
    print('handler')
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
