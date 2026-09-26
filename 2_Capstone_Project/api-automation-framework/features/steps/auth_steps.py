"""
Step definitions for features/auth.feature -- demonstrates the
authentication piece of the capstone requirements.
"""

from behave import given, when, then

from api_client.auth_api import AuthAPI
from utils.assertions import assert_status_code
from utils.data_reader import read_yaml


@given('the auth API base URL is set')
def step_set_auth_base_url(context):
    context.auth_api = AuthAPI()


@when('I send a login request with valid credentials')
def step_login_valid(context):
    creds = read_yaml("test_config.yaml")["login"]["valid_user"]
    context.response = context.auth_api.login(creds["email"], creds["password"])


@when('I send a login request with invalid credentials')
def step_login_invalid(context):
    creds = read_yaml("test_config.yaml")["login"]["invalid_user"]
    context.response = context.auth_api.login(creds["email"], creds["password"])


@then('the auth response status code should be {expected_code:d}')
def step_check_auth_status_code(context, expected_code):
    assert_status_code(context.response, expected_code)


@then('the auth response message should indicate login failure')
def step_check_login_failure_message(context):
    body = context.response.json()
    message = body.get("message", "").lower()
    assert "not found" in message or "incorrect" in message, (
        f"Expected a login-failure message, got: {body}"
    )
