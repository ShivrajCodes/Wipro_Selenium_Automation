"""
BaseAPIClient: a thin, generic wrapper around the `requests` library.

Every endpoint-specific client (UserAPI, AuthAPI, ...) inherits from
this instead of calling `requests` directly. This is what makes the
framework "reusable design" rather than a pile of one-off scripts:
  - one place that sets base URL, headers, timeout
  - one place that logs every request/response
  - one place that attaches request/response bodies to Allure reports
"""

import json

import allure
import requests

from config.config import DEFAULT_HEADERS, REQUEST_TIMEOUT
from utils.logger import logger


class BaseAPIClient:
    def __init__(self, base_url: str, headers: dict = None, timeout: int = REQUEST_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.headers = {**DEFAULT_HEADERS, **(headers or {})}
        self.timeout = timeout
        self.session = requests.Session()

    def set_auth_token(self, token: str):
        """Attach a bearer token to every subsequent request on this client."""
        self.headers["Authorization"] = f"Bearer {token}"

    def _full_url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _request(self, method: str, path: str, **kwargs):
        url = self._full_url(path)
        logger.info(f"--> {method} {url}")
        if "json" in kwargs and kwargs["json"] is not None:
            logger.debug(f"Request body: {json.dumps(kwargs['json'], indent=2)}")

        response = self.session.request(
            method=method,
            url=url,
            headers=self.headers,
            timeout=self.timeout,
            **kwargs,
        )

        logger.info(f"<-- {response.status_code} {url} ({response.elapsed.total_seconds():.3f}s)")
        self._attach_to_allure(method, url, kwargs.get("json"), response)

        return response

    @staticmethod
    def _attach_to_allure(method, url, request_body, response):
        """Attach request/response details to the Allure report for debugging."""
        allure.attach(
            f"{method} {url}\n\nRequest body:\n{json.dumps(request_body, indent=2) if request_body else 'None'}",
            name="Request",
            attachment_type=allure.attachment_type.TEXT,
        )
        try:
            body = json.dumps(response.json(), indent=2)
        except ValueError:
            body = response.text
        allure.attach(
            f"Status: {response.status_code}\n\nBody:\n{body}",
            name="Response",
            attachment_type=allure.attachment_type.TEXT,
        )

    # Thin verbs -----------------------------------------------------
    def get(self, path: str, params: dict = None):
        return self._request("GET", path, params=params)

    def post(self, path: str, json_body: dict = None):
        return self._request("POST", path, json=json_body)

    def put(self, path: str, json_body: dict = None):
        return self._request("PUT", path, json=json_body)

    def patch(self, path: str, json_body: dict = None):
        return self._request("PATCH", path, json=json_body)

    def delete(self, path: str):
        return self._request("DELETE", path)
