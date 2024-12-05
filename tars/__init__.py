"""
TARS - Task Automation and Resource Scheduler

This package provides the core functionality for task automation,
resource scheduling, and parallel execution of testing workflows.
"""

# Expose core components for easy imports
from .scheduler import Scheduler
from .registry import register

# Package metadata
__version__ = "0.1.0"
__author__ = "Zijie Zhang"
__license__ = "GPL v3"

# Provide a clean API for package usage
__all__ = [
    "Scheduler",  # Core task scheduler
    "register"    # Decorator for registering tasks
]
