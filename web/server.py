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
