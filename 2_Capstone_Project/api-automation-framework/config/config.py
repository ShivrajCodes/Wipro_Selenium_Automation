"""
Central configuration for the API Automation Framework.

Everything environment-specific (base URL, timeouts, default headers)
lives here so it's never hardcoded inside test steps or the API client.
"""

import os

# ---------------------------------------------------------------------
# Environment switch: set API_ENV=staging (or prod) as an OS env var to
# point the framework at a different base URL without changing code.
# ---------------------------------------------------------------------
ENV = os.getenv("API_ENV", "dev")

BASE_URLS = {
    "dev": "https://jsonplaceholder.typicode.com",
    # Example of a second target used for the auth/token demo scenarios
    "auth_demo": "https://automationexercise.com/api",
}

BASE_URL = BASE_URLS.get(ENV, BASE_URLS["dev"])
AUTH_BASE_URL = BASE_URLS["auth_demo"]

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

REQUEST_TIMEOUT = 10  # seconds

# Toggle verbose request/response logging (also attached to Allure reports)
DEBUG_LOGGING = True
