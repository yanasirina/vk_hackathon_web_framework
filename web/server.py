import logging
import sys

from gunicorn.app.base import BaseApplication


class Server(BaseApplication):
    def __init__(self, app, options=None):
        self.app = app
        self.options = options or {}
        super().__init__()

    def init(self, *_):
        return self.options

    def load(self):
        return self.app

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key.lower(), value)

    def configure_logging(self):
        gunicorn_error_logger = logging.getLogger('gunicorn.error')
        gunicorn_access_logger = logging.getLogger('gunicorn.access')

        app_logger = logging.getLogger('app')
        app_logger.setLevel(logging.DEBUG)

        for handler in gunicorn_error_logger.handlers:
            app_logger.addHandler(handler)

        for handler in gunicorn_access_logger.handlers:
            app_logger.addHandler(handler)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_formatter = logging.Formatter("STDOUT: %(levelname)s - %(message)s")
        stdout_handler.setFormatter(stdout_formatter)
        app_logger.addHandler(stdout_handler)

        app_logger.info("Application logging configured: logs to stdout")

    def run(self):
        self.configure_logging()

        app_logger = logging.getLogger('app')
        app_logger.info("Application started")

        super().run()
