"""
Step definitions for features/user_management.feature.

These stay thin on purpose: all HTTP logic lives in api_client/,
all assertion logic lives in utils/assertions.py. Steps just wire
Gherkin language to those reusable pieces.
"""

from behave import given, when, then

from api_client.user_api import UserAPI
from utils.assertions import (
    assert_status_code,
    assert_response_time,
    assert_field_equals,
    assert_matches_schema,
)
from utils.data_reader import read_json


@given('the API base URL is set')
def step_set_base_url(context):
    context.user_api = UserAPI()


@when('I send a GET request to fetch all users')
def step_get_all_users(context):
    context.response = context.user_api.get_all_users()


@when('I send a GET request to fetch user with id {user_id:d}')
def step_get_user_by_id(context, user_id):
    context.response = context.user_api.get_user(user_id)


@when('I send a POST request to create a user with valid data')
def step_create_user(context):
    payload = read_json("users.json")["valid_new_user"]
    context.response = context.user_api.create_user(payload)


@when('I send a PUT request to update user with id {user_id:d} with valid data')
def step_update_user(context, user_id):
    payload = read_json("users.json")["update_payload"]
    context.response = context.user_api.update_user(user_id, payload)


@when('I send a DELETE request to remove user with id {user_id:d}')
def step_delete_user(context, user_id):
    context.response = context.user_api.delete_user(user_id)


@then('the response status code should be {expected_code:d}')
def step_check_status_code(context, expected_code):
    assert_status_code(context.response, expected_code)


@then('the response should match the "{schema_filename}" schema')
def step_check_schema(context, schema_filename):
    assert_matches_schema(context.response.json(), schema_filename)


@then('the response time should be under {max_ms:d} ms')
def step_check_response_time(context, max_ms):
    assert_response_time(context.response, max_ms)


@then('the response field "{field}" should equal {value}')
def step_check_field_equals(context, field, value):
    # Strip surrounding quotes if the value was written as a string in the .feature file
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    else:
        # try to interpret as int, fall back to raw string
        try:
            value = int(value)
        except ValueError:
            pass
    assert_field_equals(context.response.json(), field, value)
