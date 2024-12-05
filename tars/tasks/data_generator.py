"""
data_generator.py

Generates input data for the LayerNorm operator.
"""

import numpy as np
from tars.registry import register
from tars.common import TASKTYPE

@register(TASKTYPE.DATA_GENERATION, "LayerNorm")
def layernorm(batch_size=4, feature_size=128):
    """
    Generates random inputs for LayerNorm.

    Args:
        batch_size (int): The number of rows in the input tensor.
        feature_size (int): The number of columns in the input tensor.

    Returns:
        numpy.ndarray: A tensor of shape (batch_size, feature_size).
    """
    print("[Data Generator] Generating inputs for LayerNorm.")
    inputs = np.random.rand(batch_size, feature_size).astype(np.float32)
    return inputs
