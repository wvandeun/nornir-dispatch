from __future__ import annotations

import importlib
import logging
import re

from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, Optional, Union, Callable, Type

from nornir.core.task import Result, Task

from nornir_dispatcher.exceptions import PlatformNotFoundError, TaskNotFoundError

LOGGER = logging.getLogger(__name__)


@dataclass
class TaskElement:
    task: Callable
    origin: Optional[str]


REGEX_VALID_FUNCTION_STRING = r"^.*\..*\..*$"


@dataclass
class Registry:
    tasks: Dict[str, Dict[str, TaskElement]] = field(
        default_factory=lambda: defaultdict(dict)
    )

    def _register_task_func(
        self, platform: str, action: str, task: Callable, origin: str = None
    ) -> bool:
        # TODO check if a task already exist for this task_name
        self.tasks[platform][action] = TaskElement(task=task, origin=origin)

        return True

    def register_task(
        self, platform: str, action: str, task: Union[str, Callable]
    ) -> bool:
        if isinstance(task, Callable):
            return self._register_task_func(platform=platform, action=action, task=task)

        elif isinstance(task, str):
            module_name, function_name = task.rsplit(".", 1)
            task_function = getattr(importlib.import_module(module_name), function_name)

            if not task_function:
                raise Exception(
                    f"Unable to locate the task function {task}, preemptively failed."
                )

            return self._register_task_func(
                platform=platform, action=action, task=task_function, origin=task
            )

    def register_tasks(self, platform: str, driver: Union[str, Type[object]]) -> bool:
        if isinstance(driver, object):
            for key, value in driver.__dict__.items():
                if not isinstance(value, staticmethod):
                    continue

                getattr(driver, key)
                self._register_task_func(
                    platform=platform, action=key, task=getattr(driver, key), origin=driver.__name__
                )

        elif isinstance(driver, str):
            pass

    def get_task(self, platform: str, action: str) -> Callable:
        if platform not in self.tasks:
            raise PlatformNotFoundError(platform=platform)

        if action not in self.tasks[platform]:
            raise TaskNotFoundError(platform=platform, action=action)

        return self.tasks[platform][action].task

    def has_task(self, platform: str, action: str):
        if platform in self.tasks and action in self.tasks[platform]:
            return True

        return False


registry = Registry()