"""
Centralized endpoint paths.

Keeping every path as a constant here means a single source of truth --
if an endpoint changes, it changes in exactly one place.
"""


class UserEndpoints:
    USERS = "/users"
    USER_BY_ID = "/users/{user_id}"


class AuthEndpoints:
    LOGIN = "/login"
    VERIFY_LOGIN = "/verifyLogin"
