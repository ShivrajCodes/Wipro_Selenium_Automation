"""
Behave environment hooks.

Behave automatically discovers and runs this file. Allure result
collection itself is handled by passing `-f allure_behave.formatter:AllureFormatter`
on the command line (see behave.ini) -- this file just adds our own
logging/setup around it.
"""

from utils.logger import logger


def before_all(context):
    logger.info("=" * 70)
    logger.info("Starting API Automation Test Run")
    logger.info("=" * 70)


def before_scenario(context, scenario):
    logger.info(f"--- Starting scenario: {scenario.name} ---")


def after_scenario(context, scenario):
    status = "PASSED" if scenario.status == "passed" else "FAILED"
    logger.info(f"--- Scenario '{scenario.name}' {status} ---")


def after_all(context):
    logger.info("=" * 70)
    logger.info("Test Run Complete")
    logger.info("=" * 70)
