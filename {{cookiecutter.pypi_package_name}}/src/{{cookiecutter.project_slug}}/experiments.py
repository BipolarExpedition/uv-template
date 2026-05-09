from collections.abc import Callable
from typing import Any
from .mylogging import logger


EXPERIMENT_LIST: dict [str, Callable[..., Any]] = {}

def experiment_1() -> None:
    logger.warning("This is experiment 1")
    return

EXPERIMENT_LIST["exp1"] = experiment_1
EXPERIMENT_LIST["1"] = experiment_1