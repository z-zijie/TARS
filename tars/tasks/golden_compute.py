"""
golden_compute.py

Golden reference computation for the LayerNorm operator.
"""

import numpy as np
from tars.registry import register
from tars.common import TASKTYPE

@register(TASKTYPE.GOLDEN, "LayerNorm")
def layernorm(inputs, epsilon=1e-5):
    """
    Golden function for LayerNorm operator.

    Args:
        inputs (numpy.ndarray): Input tensor (e.g., shape [N, D]).
        epsilon (float): A small value to avoid division by zero.

    Returns:
        numpy.ndarray: The normalized tensor (same shape as input).
    """
    print("[Golden Compute] Computing golden output for LayerNorm.")
    mean = np.mean(inputs, axis=-1, keepdims=True)
    variance = np.var(inputs, axis=-1, keepdims=True)
    normalized = (inputs - mean) / np.sqrt(variance + epsilon)
    return normalized
