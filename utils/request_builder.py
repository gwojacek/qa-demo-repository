import os
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

from requests import Response, Session


class RequestMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class Request:
    def __init__(self, method: RequestMethod, domain: str = None):
        if domain is None:
            domain = os.environ.get("ADDRESS")
            if not domain:
                raise RuntimeError("Required env var ADDRESS is not set!")
        self._domain = domain
        self._method = method
        self._path = None
        self._headers = {}
        self._default_headers = {"Content-Type": "application/json"}
        self._params = None
        self._auth = None
        self._json = None
        self._data = None
        self._cookies = None
        self._allow_redirects = True

    def json(self, json: dict) -> "Request":
        self._json = json
        self._data = None  # Clear form data if JSON is set
        return self

    def data(self, data: dict) -> "Request":
        self._data = data
        self._json = None  # Clear JSON if form data is set
        return self

    def headers(self, headers: dict) -> "Request":
        self._headers = headers
        return self

    def default_headers(self) -> "Request":
        self._headers.update(self._default_headers)
        return self

    def auth(self, token: str) -> "Request":
        if self._headers is None:
            self._headers = {}
        self._headers["Authorization"] = f"Bearer {token}"
        return self

    def params(self, params: dict) -> "Request":
        self._params = params
        return self

    def cookies(self, **kwargs) -> "Request":
        self._cookies = self._headers.update(**kwargs)
        return self

    def path(self, path: str) -> "Request":
        self._path = path
        return self

    def allow_redirects(self, allow: bool) -> "Request":
        self._allow_redirects = allow
        return self

    def _prepare_url(self) -> str:
        # Accept either full URL or domain only in ADDRESS
        if self._domain.startswith("http://") or self._domain.startswith("https://"):
            base = self._domain
        else:
            base = f"https://{self._domain}"
        return urljoin(base, self._path)

    def send(self) -> Response:
        response = Session().request(
            method=self._method,
            url=self._prepare_url(),
            headers=self._headers,
            params=self._params,
            cookies=self._cookies,
            json=self._json,
            data=self._data,
            auth=self._auth,
            timeout=30,
            verify=False,
            allow_redirects=self._allow_redirects,
        )
        return response
