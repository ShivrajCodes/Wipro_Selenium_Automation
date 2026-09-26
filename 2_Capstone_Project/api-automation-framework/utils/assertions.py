"""
Reusable assertion helpers.

Centralizing assertions keeps step definitions short and readable, and
means every failure message is consistent and debuggable.
"""

from utils.logger import logger
from utils.schema_validator import validate_schema


def assert_status_code(response, expected_code: int):
    actual = response.status_code
    assert actual == expected_code, (
        f"Expected status code {expected_code}, got {actual}. "
        f"Response body: {response.text}"
    )
    logger.debug(f"Status code assertion passed: {actual} == {expected_code}")


def assert_response_time(response, max_ms: int = 2000):
    elapsed_ms = response.elapsed.total_seconds() * 1000
    assert elapsed_ms <= max_ms, (
        f"Response took {elapsed_ms:.0f}ms, expected under {max_ms}ms"
    )
    logger.debug(f"Response time assertion passed: {elapsed_ms:.0f}ms")


def assert_field_equals(response_json: dict, field: str, expected_value):
    actual_value = response_json.get(field)
    assert actual_value == expected_value, (
        f"Expected field '{field}' to equal '{expected_value}', got '{actual_value}'"
    )
    logger.debug(f"Field assertion passed: {field} == {expected_value}")


def assert_field_present(response_json: dict, field: str):
    assert field in response_json, f"Expected field '{field}' to be present in response"


def assert_matches_schema(response_json, schema_filename: str):
    """The 'deal-breaking' contract-testing assertion."""
    is_valid, error = validate_schema(response_json, schema_filename)
    assert is_valid, f"Schema validation failed against '{schema_filename}': {error}"
