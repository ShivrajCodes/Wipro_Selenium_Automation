"""
AuthAPI: demonstrates authentication handling.

jsonplaceholder.typicode.com has no real auth, so this client targets
automationexercise.com/api, which has a real login/verify endpoint --
useful for showing token/session handling, which a pure CRUD demo
against jsonplaceholder can't demonstrate on its own.
"""

from api_client.base_client import BaseAPIClient
from config.config import AUTH_BASE_URL
from config.endpoints import AuthEndpoints


class AuthAPI(BaseAPIClient):
    def __init__(self):
        super().__init__(base_url=AUTH_BASE_URL)

    def login(self, email: str, password: str):
        payload = {"email": email, "password": password}
        return self.post(AuthEndpoints.VERIFY_LOGIN, json_body=payload)
