import logging
import sys
from typing import Union, Any, Optional
import datetime

from loguru import logger
from rich.logging import RichHandler
from rich.console import Console

"""
Setup logging to use loguru for logging, with rich for pretty console output.

Intercepts standard logging calls.
"""

console = Console()

# "<green>{time:MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",

def setup_logging(level: int | str = logging.INFO,
            console_level: Optional[int | str] = None,
            log_file: Optional[str] = None,
            format_console: Optional[str] = "{message}",
            format_logs: Optional[str] = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            console_locals: bool = False,
            enqueue: bool = True,
            console_tracebacks: bool = False,
            console_markup: bool = True,
            console_omit_repeated_times: bool = False,
            console_show_time: bool = True,
            console_show_path: bool = False,
            loguru_tracebacks: bool = False,
            loguru_locals: bool = False,
            loguru_rotation: Optional[str | int | datetime.time | datetime.timedelta] = "10 MB",
            loguru_retention: Optional[str | int | datetime.timedelta] = "10 days",
            loguru_compression: str | callable = "gz",  # "gz", "bz2", "xz", "lzma", "tar", "tar.gz", "tar.bz2", "tar.xz", "zip"
            loguru_watch_files: bool = False,
            loguru_delay_file_creation: bool = False,
        ) -> None:
    """Setup logging with loguru and rich.

    Disclosure:
        Most of this code is adapted from online examples, loguru documentation, and Gemini's
        suggestions. I am not an expert in logging, loguru, or rich.
    """

    # Intercept standard logging
    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord):
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            frame, depth = logging.currentframe(), 2
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back  # type: ignore[union-attr]
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    logger.remove()
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Add console handler

    # Hanlder for my console output
    handler_console = RichHandler(
        console=console,
        level=console_level if console_level is not None else level,
        show_level=True,
        show_path=console_show_path,
        show_time=console_show_time,
        rich_tracebacks = console_tracebacks,
        tracebacks_show_locals = console_locals,
        markup = console_markup,
        omit_repeated_times = console_omit_repeated_times,
    )
    handler_console.setFormatter(logging.Formatter(format_console))

    logger.add(
        handler_console,
        format=format_console,
        level=console_level if console_level is not None else level,
        backtrace=console_tracebacks,
        diagnose=console_locals,
        enqueue=enqueue
    )
    
    # Add log file handler
    if log_file:
        logger.add(
            log_file,
            level=level,
            format=format_logs,
            rotation=loguru_rotation,
            retention=loguru_retention,
            compression=loguru_compression,
            enqueue=enqueue,
            backtrace=loguru_tracebacks,
            diagnose=loguru_locals,
            watch=loguru_watch_files,
            delay=loguru_delay_file_creation,
        )

# def setup_logging(
#     level: Union[int, str] = logging.INFO,
#     log_format: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
#                       "<level>{level: <8}</level> | "
#                       "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
#                       "<level>{message}</level>",
#     date_format: str = "YYYY-MM-DD HH:mm:ss.SSS",
#     log_file: str | None = None,
#     file_log_level: Union[int, str] = logging.DEBUG,
#     file_log_format: str = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
#     file_date_format: str = "YYYY-MM-DD HH:mm:ss.SSS",
# ) -> None:
#     class InterceptHandler(logging.Handler):
#         def emit(self, record: logging.LogRecord) -> None:
#             try:
#                 level = logger.level(record.levelname).name
#             except ValueError:
#                 level = record.levelno

#             frame, depth = logging.currentframe(), 2
#             while frame.f_code.co_filename == logging.__file__:
#                 frame = frame.f_back  # type: ignore[union-attr]
#                 depth += 1

#             logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

#     logging.root.handlers = [InterceptHandler()]
#     logging.root.setLevel(level)

#     rich_handler = RichHandler(
#         rich_tracebacks=True,
#         tracebacks_show_locals=True,
#         markup=True,
#         log_time_format=date_format,
#     )
#     rich_handler.setLevel(level)
#     rich_handler.setFormatter(logging.Formatter(log_format))

#     logging.getLogger().addHandler(rich_handler)

#     if log_file:
#         logger.add(
#             log_file,
#             level=file_log_level,
#             format=file_log_format,
#             datefmt=file_date_format,
#             rotation="10 MB",
#             retention="10 days",
#             compression="zip",
#         )