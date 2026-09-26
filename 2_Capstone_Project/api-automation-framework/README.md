# Python API Automation Framework — Requests + Behave BDD + Allure

A reusable API test automation framework built for the User Management
API at [jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com/),
with an authentication demo against
[automationexercise.com/api](https://automationexercise.com/api_list).

## Key Features

- **Requests-based API client layer** — reusable, DRY HTTP wrapper (`api_client/`)
- **Behave BDD** — plain-English `Given/When/Then` scenarios (`features/`)
- **JSON Schema (contract) validation** — verifies response *structure*, not just status codes (`schemas/`, `utils/schema_validator.py`)
- **Allure reporting** — request/response bodies attached to every step
- **Data-driven testing** — payloads/credentials loaded from JSON/YAML (`test_data/`)
- **Authentication handling** — bearer token support in the base client, login scenarios in `auth.feature`
- **Centralized config** — base URLs, timeouts, endpoints all in one place (`config/`)

## Project Structure

```
api-automation-framework/
├── features/
│   ├── user_management.feature
│   ├── auth.feature
│   └── steps/
│       ├── user_steps.py
│       └── auth_steps.py
├── api_client/
│   ├── base_client.py
│   ├── user_api.py
│   └── auth_api.py
├── config/
│   ├── config.py
│   └── endpoints.py
├── schemas/
│   ├── user_schema.json
│   ├── user_list_schema.json
│   ├── created_user_schema.json
│   └── error_schema.json
├── test_data/
│   ├── users.json
│   └── test_config.yaml
├── utils/
│   ├── logger.py
│   ├── assertions.py
│   ├── schema_validator.py
│   └── data_reader.py
├── environment.py
├── behave.ini
├── requirements.txt
└── reports/allure-results/
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

You'll also need the **Allure commandline tool** installed separately to
generate/view the HTML report (it's a Java-based CLI, not a pip package):

```bash
# macOS
brew install allure

# Or download manually:
# https://github.com/allure-framework/allure2/releases
```

## Running the tests

Run everything:
```bash
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results
```

Run only a tagged subset (e.g. just smoke tests):
```bash
behave --tags=@smoke -f allure_behave.formatter:AllureFormatter -o reports/allure-results
```

Run without Allure (plain console output):
```bash
behave
```

## Viewing the Allure report

```bash
allure serve reports/allure-results
```

This opens an interactive HTML report in your browser showing every
scenario, step, attached request/response payload, and timing.

## Switching environments

The base URL is controlled by an environment variable:

```bash
API_ENV=dev behave        # default -> jsonplaceholder.typicode.com
```

Add more entries to `BASE_URLS` in `config/config.py` to point at a
staging/prod environment without touching any test code.

## Notes on jsonplaceholder.typicode.com

This is a fake/mock API — POST/PUT/DELETE requests are accepted and
return realistic responses, but nothing is actually persisted server-side.
That's fine for this framework's purpose: it's demonstrating correct
request construction, response validation, and reporting, not real
data persistence.

## Extending the framework

To test a new resource (e.g. `/posts`):
1. Add path constants to `config/endpoints.py`
2. Create `api_client/post_api.py` following the `UserAPI` pattern
3. Add JSON schema(s) to `schemas/`
4. Write a `.feature` file + matching step definitions
5. Done — no changes needed anywhere else
