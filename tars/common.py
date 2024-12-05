"""
common.py

Shared constants and enumerations for TARS framework.
"""

from enum import Enum

class TASKTYPE(Enum):
    """
    Enumeration for task types in the TARS framework.
    """
    GOLDEN = "golden"              # Tasks for computing golden (reference) outputs
    KERNEL = "kernel"              # Tasks for kernel execution
    DATA_GENERATION = "data_generation"  # Tasks for generating inputs
    OTHER = "other"                # Miscellaneous tasks
