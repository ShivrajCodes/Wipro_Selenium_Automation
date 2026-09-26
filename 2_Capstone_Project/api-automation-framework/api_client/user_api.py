"""
UserAPI: endpoint-specific client for the User Management API
(https://jsonplaceholder.typicode.com/users).

Step definitions call methods on this class -- they never touch
`requests` or raw URLs directly. This is the "service layer" that
makes adding a new test scenario a one-line call rather than
duplicated request-building code.
"""

from api_client.base_client import BaseAPIClient
from config.config import BASE_URL
from config.endpoints import UserEndpoints


class UserAPI(BaseAPIClient):
    def __init__(self):
        super().__init__(base_url=BASE_URL)

    def get_all_users(self):
        return self.get(UserEndpoints.USERS)

    def get_user(self, user_id: int):
        path = UserEndpoints.USER_BY_ID.format(user_id=user_id)
        return self.get(path)

    def create_user(self, payload: dict):
        return self.post(UserEndpoints.USERS, json_body=payload)

    def update_user(self, user_id: int, payload: dict):
        path = UserEndpoints.USER_BY_ID.format(user_id=user_id)
        return self.put(path, json_body=payload)

    def partial_update_user(self, user_id: int, payload: dict):
        path = UserEndpoints.USER_BY_ID.format(user_id=user_id)
        return self.patch(path, json_body=payload)

    def delete_user(self, user_id: int):
        path = UserEndpoints.USER_BY_ID.format(user_id=user_id)
        return self.delete(path)
