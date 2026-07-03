"""Generation and logging of classification confusion matrices."""

from __future__ import annotations

import numpy as np
from typing import List, Union
from sklearn.metrics import confusion_matrix # type: ignore

def get_confusion_matrix(
    y_true: Union[np.ndarray, list],
    y_pred: Union[np.ndarray, list],
) -> List[List[int]]:
    """Generate confusion matrix as a nested list of integers."""
    cm = confusion_matrix(y_true, y_pred)
    return cm.tolist()
