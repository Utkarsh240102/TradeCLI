import logging
import sys
from pathlib import Path


def setup_logging() -> None:
    """Configure file (DEBUG) and console (INFO) handlers for the trading_bot logger."""
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return  # Prevent duplicate handlers on repeated calls

    # File handler for detailed logs (DEBUG and above)
    log_path = Path("logs/trading_bot.log")
    log_path.parent.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    ))

    # Console handler for clean, user-facing output (INFO and above)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        fmt="%(levelname)-5s %(message)s"
    ))

    # Attach handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
