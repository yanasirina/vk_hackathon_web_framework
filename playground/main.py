import web

import os


router = web.Router()


@router.route('/')
def home(environ):
    return 'Welcome to the home page!'


@router.route('/hello')
def hello(environ):
    name = environ.get('QUERY_STRING', 'world').split('=')[-1]
    return f'Hello, {name}!'


@router.route('/about')
def about(environ):
    return 'This i a simple Router with Gunicorn example.'


def main() -> None:
    options = {
        'bind': '0.0.0.0:8080',
        'workers': os.cpu_count(),
        'loglevel': 'info',
    }

    web.Server(router, options).run()


if __name__ == '__main__':
    main()
