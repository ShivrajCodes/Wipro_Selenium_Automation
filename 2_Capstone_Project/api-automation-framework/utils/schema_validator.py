"""
JSON Schema validation utility.

This is what turns a status-code-only test suite into real contract
testing: it verifies the *shape* of an API response (required fields,
correct types, no silently-broken contracts) rather than just whether
the request succeeded.
"""

import json
import os
from typing import Tuple, Optional

from jsonschema import validate, ValidationError

from utils.logger import logger

SCHEMA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "schemas")


def load_schema(schema_filename: str) -> dict:
    """Load a JSON schema file from the /schemas directory."""
    schema_path = os.path.join(SCHEMA_DIR, schema_filename)
    with open(schema_path, "r") as f:
        return json.load(f)


def validate_schema(response_json, schema_filename: str) -> Tuple[bool, Optional[str]]:
    """
    Validate response_json against the named schema file.

    Returns:
        (True, None) if valid.
        (False, error_message) if invalid -- never raises, so callers
        can decide how to assert/report the failure (e.g. attach to Allure).
    """
    schema = load_schema(schema_filename)
    try:
        validate(instance=response_json, schema=schema)
        logger.debug(f"Schema validation PASSED for {schema_filename}")
        return True, None
    except ValidationError as e:
        error_message = f"{e.message} (at path: {list(e.absolute_path)})"
        logger.error(f"Schema validation FAILED for {schema_filename}: {error_message}")
        return False, error_message
