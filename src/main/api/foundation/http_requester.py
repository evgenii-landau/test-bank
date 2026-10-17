from typing import Callable, Dict

from src.main.api.foundation.endpoint import Endpoint


class HttpRequester:
    def __init__(self, endpoint: Endpoint, request_spec: Dict, response_spec: Callable):
        self.endpoint = endpoint
        self.request_spec = request_spec
        self.response_spec = response_spec
