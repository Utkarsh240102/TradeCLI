import logging
import pytest
from unittest.mock import patch


def pytest_configure(config):
    """Prevent tests from writing to the deliverable log file."""
    logger = logging.getLogger("trading_bot")
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)


def pytest_runtest_setup(item):
    """Strip any handlers added by setup_logging() before each test runs."""
    logger = logging.getLogger("trading_bot")
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)


@pytest.fixture(autouse=True)
def disable_logging_setup():
    """Mock setup_logging as a no-op so tests never create the file handler."""
    with patch("cli.setup_logging", return_value=None):
        yield

    # Clean up any handlers that leaked through anyway
    logger = logging.getLogger("trading_bot")
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)
