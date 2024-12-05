"""
scheduler.py

This module provides the Scheduler class, which manages task execution,
dependency resolution, and workflow orchestration in TARS.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from tars.registry import get_task
from tars.common import TASKTYPE

class Scheduler:
    """
    Scheduler for managing task execution and dependencies.
    """
    def __init__(self, max_workers=4):
        """
        Initialize the scheduler.

        Args:
            max_workers (int): Maximum number of threads for parallel execution.
        """
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.task_queues = {}  # Maps stage names to their task queues
        self.results = {}      # Maps task identifiers to results

    def add_stage(self, task_type, task_name):
        """
        Add a stage to the scheduler by creating a queue for its tasks.

        Args:
            task_type (TASKTYPE): The type of the task (e.g., TASKTYPE.GOLDEN).
            task_name (str): The name of the task stage.
        """
        stage_key = (task_type, task_name)
        if stage_key in self.task_queues:
            raise ValueError(f"Stage '{task_name}' of type '{task_type.value}' already exists.")
        self.task_queues[stage_key] = Queue()
        print(f"[Scheduler] Stage '{task_name}' added under type '{task_type.value}'.")

    def submit_task(self, task_type, task_name, *args, **kwargs):
        """
        Submit a task to the appropriate stage for execution.

        Args:
            task_type (TASKTYPE): The type of the task (e.g., TASKTYPE.GOLDEN).
            task_name (str): The name of the task stage.
            *args: Positional arguments for the task function.
            **kwargs: Keyword arguments for the task function.

        Returns:
            concurrent.futures.Future: A future object representing the task execution.
        """
        stage_key = (task_type, task_name)
        if stage_key not in self.task_queues:
            raise KeyError(f"Stage '{task_name}' of type '{task_type.value}' does not exist.")

        # Retrieve the task function from the registry
        task_func = get_task(task_type, task_name)

        # Submit the task to the executor
        future = self.executor.submit(task_func, *args, **kwargs)

        # Store the future in the task queue
        self.task_queues[stage_key].put(future)
        print(f"[Scheduler] Task submitted to stage '{task_name}' under type '{task_type.value}'.")
        return future

    def wait_for_all(self):
        """
        Wait for all tasks in all stages to complete.
        """
        for stage_key, queue in self.task_queues.items():
            task_type, task_name = stage_key
            print(f"[Scheduler] Waiting for tasks in stage '{task_name}' of type '{task_type.value}'.")
            while not queue.empty():
                future = queue.get()
                try:
                    result = future.result()  # Wait for task to complete
                    self.results[stage_key] = result
                except Exception as e:
                    print(f"[Scheduler] Task in stage '{task_name}' failed: {e}")

    def get_results(self, task_type=None, task_name=None):
        """
        Retrieve results from completed tasks.

        Args:
            task_type (TASKTYPE, optional): Filter by task type.
            task_name (str, optional): Filter by task name.

        Returns:
            dict: Results matching the filters.
        """
        if task_type and task_name:
            stage_key = (task_type, task_name)
            return self.results.get(stage_key, None)
        elif task_type:
            return {key: value for key, value in self.results.items() if key[0] == task_type}
        return self.results
