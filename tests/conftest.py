import logging

def pytest_configure(config):
    """Prevent tests from writing to the deliverable log file."""
    logger = logging.getLogger("trading_bot")
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
