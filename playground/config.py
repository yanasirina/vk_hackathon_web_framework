import os

from dotenv import load_dotenv


load_dotenv()

HOST = os.getenv('HOST', default='0.0.0.0')
PORT = os.getenv('PORT', default='8080')
WORKERS_COUNT = os.getenv('WORKERS_COUNT', default=os.cpu_count())
LOG_LEVEL = os.getenv('LOG_LEVEL', default='info')


def get_config() -> dict:
    config = {
        'bind': f'{HOST}:{PORT}',
        'workers': WORKERS_COUNT,
        'loglevel': LOG_LEVEL,
    }
    return config
