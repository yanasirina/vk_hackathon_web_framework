import datetime
import os

import web
import web.responses


app = web.Router()


@app.route('/main')
def html_example(_request):
    response = web.responses.HTMLResponse(
        template_path='templates/index.html',
        context={'today_date': datetime.date.today()}
    )
    return response


@app.route('/hello')
def json_example(_request):
    response = web.responses.JsonResponse({'message': 'hello, world!'})
    return response


@app.not_found
def custom_404(_request):
    response = web.responses.JsonResponse({'error': 'route not found'})
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
