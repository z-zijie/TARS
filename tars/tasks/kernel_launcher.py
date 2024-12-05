"""
kernel_launcher.py

Simulates kernel execution for the LayerNorm operator.
"""

import numpy as np
from tars.registry import register
from tars.common import TASKTYPE

@register(TASKTYPE.KERNEL, "LayerNorm")
def layernorm(inputs, epsilon=1e-5):
    """
    Simulates kernel execution for LayerNorm operator.

    Args:
        inputs (numpy.ndarray): Input tensor (e.g., shape [N, D]).
        epsilon (float): A small value to avoid division by zero.

    Returns:
        numpy.ndarray: The output tensor (same shape as input).
    """
    print("[Kernel Launcher] Simulating LayerNorm kernel execution.")
    # Simulate kernel computation (same logic as golden but assume it's on hardware)
    mean = np.mean(inputs, axis=-1, keepdims=True)
    variance = np.var(inputs, axis=-1, keepdims=True)
    normalized = (inputs - mean) / np.sqrt(variance + epsilon)
    return normalized
