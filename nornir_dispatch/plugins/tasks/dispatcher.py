from nornir.core.task import Result, Task
from nornir_dispatch import registry


def dispatcher(task: Task, action: str, *args, **kwargs) -> Result:  # type: ignore
    """Helper Task to retrieve a given Nornir task for a given platform.

    Args:
        task (Task):  Nornir Task object.
        action (str):  The string value of the action to execute.

    Returns:
        Result: Nornir Task result.
    """
    task.name = action
    task_to_run = registry.get_task(platform=task.host.platform, action=action)
    return task_to_run(task=task, *args, **kwargs)  # type: ignore

