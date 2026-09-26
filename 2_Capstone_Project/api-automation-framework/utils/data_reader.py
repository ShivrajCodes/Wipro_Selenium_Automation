"""
Loads test data (payloads, parameters) from files in /test_data so tests
stay data-driven instead of hardcoding JSON bodies inline in steps.
"""

import json
import os

import yaml

TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_data")


def read_json(filename: str) -> dict:
    path = os.path.join(TEST_DATA_DIR, filename)
    with open(path, "r") as f:
        return json.load(f)


def read_yaml(filename: str) -> dict:
    path = os.path.join(TEST_DATA_DIR, filename)
    with open(path, "r") as f:
        return yaml.safe_load(f)
