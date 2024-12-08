import logging
import sys

from gunicorn.app.base import BaseApplication
from typing import Callable, Optional, Dict, Any


class Server(BaseApplication):
    app: Callable
    options: Optional[Dict[str, Any]]

    def __init__(self, app: Callable, options: Optional[Dict[str, Any]] = None) -> None:
        self.app = app
        self.options = options or {}
        super().__init__()

    def init(self, *_) -> Dict[str, Any]:
        return self.options

    def load(self) -> Callable:
        return self.app

    def load_config(self) -> None:
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

    def run(self) -> None:
        self.configure_logging()

        app_logger = logging.getLogger('app')
        app_logger.info("Application started")

        super().run()
