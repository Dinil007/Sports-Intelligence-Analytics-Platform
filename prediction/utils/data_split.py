"""Train-test split wrappers for regression and classification datasets."""

from __future__ import annotations

import pandas as pd
from typing import Tuple, Union, Optional
from sklearn.model_selection import train_test_split # type: ignore
from prediction.config import config

def split_dataset(
    df: pd.DataFrame,
    target_col: str,
    test_size: float = config.DEFAULT_TEST_SIZE,
    stratify: bool = False,
    random_state: int = config.RANDOM_STATE,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split a DataFrame into train and test features (X) and target (y)."""
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    stratify_y = y if stratify else None
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=stratify_y
    )
    
    return X_train, X_test, y_train, y_test
