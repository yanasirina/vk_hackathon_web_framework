import os

import web


app = web.Router()


@app.route('/hello')
def json_example(request, response):
    _ = request.method
    response.content_type = 'application/json'
    response.json = {'message': 'hello, world!'}


@app.not_found
def custom_404(request, response):
    _ = request.method
    response.content_type = 'application/json'
    response.json = {'error': 'route not found'}


def main() -> None:
    config = {
        'bind': '0.0.0.0:8080',
        'workers': os.cpu_count(),
        'loglevel': 'info',
    }

    web.Server(app, config).run()


if __name__ == '__main__':
    main()
