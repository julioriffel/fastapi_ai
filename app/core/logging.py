import logging
import os
import sys
from types import FrameType

from loguru import logger

from app.core.config import settings


def setup_logging() -> None:
    # Remove default handlers
    logger.remove()

    # Add stdout handler with specific format
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
    )

    # Ensure log directory exists
    if settings.LOG_PATH:
        log_dir = os.path.dirname(settings.LOG_PATH)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

    # Add file handler with rotation, retention, and compression
    logger.add(
        settings.LOG_PATH,
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        compression="zip",
        serialize=True,  # Serialize logs as JSON
        level="INFO",
    )

    # Intercept standard logging
    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            try:
                level: str | int = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            frame: FrameType | None = sys._getframe(6)
            depth = 6
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
