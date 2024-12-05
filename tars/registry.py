"""
registry.py

This module provides task registration and retrieval mechanisms for TARS.
It supports task categorization by types (e.g., GOLDEN, KERNEL, DATA_GENERATION)
and ensures centralized management of all registered tasks.
"""

from tars.common import TASKTYPE

# Task registry dictionary, categorized by task types
TASK_REGISTRY = {task_type: {} for task_type in TASKTYPE}

def register(task_type, task_name):
    """
    Decorator to register a task function under a specific type and name.

    Args:
        task_type (TASKTYPE): The type of the task (e.g., TASKTYPE.GOLDEN).
        task_name (str): The unique name of the task.

    Returns:
        function: The original function, unmodified.
    """
    def decorator(func):
        # Ensure the task type exists in the registry
        if task_type not in TASK_REGISTRY:
            raise ValueError(f"Invalid task type: {task_type}")

        # Check for duplicate task names
        if task_name in TASK_REGISTRY[task_type]:
            raise ValueError(f"Task '{task_name}' already registered under type '{task_type.value}'.")

        # Register the task
        TASK_REGISTRY[task_type][task_name] = func
        print(f"[Registry] Task '{task_name}' registered under type '{task_type.value}'.")
        return func
    return decorator

def get_task(task_type, task_name):
    """
    Retrieve a registered task function by its type and name.

    Args:
        task_type (TASKTYPE): The type of the task (e.g., TASKTYPE.GOLDEN).
        task_name (str): The name of the task.

    Returns:
        function: The registered task function.

    Raises:
        KeyError: If the task is not found in the registry.
    """
    if task_type not in TASK_REGISTRY or task_name not in TASK_REGISTRY[task_type]:
        raise KeyError(f"Task '{task_name}' is not registered under type '{task_type.value}'.")
    return TASK_REGISTRY[task_type][task_name]

def list_tasks(task_type=None):
    """
    List all registered tasks, optionally filtered by task type.

    Args:
        task_type (TASKTYPE, optional): If specified, lists tasks for that type only.

    Returns:
        list or dict: A list of tasks for the specified type, or a dictionary of all tasks by type.
    """
    if task_type:
        return list(TASK_REGISTRY[task_type].keys())
    return {task_type.value: list(tasks.keys()) for task_type, tasks in TASK_REGISTRY.items()}
