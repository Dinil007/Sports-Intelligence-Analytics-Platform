"""Preprocessing pipelines for missing values, encoding, and scaling."""

from __future__ import annotations

import pandas as pd
import numpy as np
from typing import List, Tuple, Dict, Any, Union
from sklearn.impute import SimpleImputer # type: ignore
from sklearn.preprocessing import StandardScaler, OneHotEncoder # type: ignore

class DataPreprocessor:
    """Preprocess raw football data using standard sklearn transformers."""
    
    def __init__(self, numeric_cols: List[str], categorical_cols: List[str]) -> None:
        self.numeric_cols = numeric_cols
        self.categorical_cols = categorical_cols
        
        self.num_imputer = SimpleImputer(strategy="mean")
        self.cat_imputer = SimpleImputer(strategy="most_frequent")
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        self.is_fitted = False

    def fit(self, df: pd.DataFrame) -> DataPreprocessor:
        """Fit all preprocessing transformers to the training dataframe."""
        # Fit numeric pipeline
        if self.numeric_cols:
            num_data = df[self.numeric_cols]
            self.num_imputer.fit(num_data)
            imputed_num = self.num_imputer.transform(num_data)
            self.scaler.fit(imputed_num)
            
        # Fit categorical pipeline
        if self.categorical_cols:
            cat_data = df[self.categorical_cols].astype(str)
            self.cat_imputer.fit(cat_data)
            imputed_cat = self.cat_imputer.transform(cat_data)
            self.encoder.fit(imputed_cat)
            
        self.is_fitted = True
        return self

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """Apply pre-fitted preprocessing transformations to a dataframe."""
        if not self.is_fitted:
            raise RuntimeError("Preprocessor must be fitted before transforming.")
            
        parts = []
        
        # Transform numeric features
        if self.numeric_cols:
            num_data = df[self.numeric_cols]
            imputed_num = self.num_imputer.transform(num_data)
            scaled_num = self.scaler.transform(imputed_num)
            parts.append(scaled_num)
            
        # Transform categorical features
        if self.categorical_cols:
            cat_data = df[self.categorical_cols].astype(str)
            imputed_cat = self.cat_imputer.transform(cat_data)
            encoded_cat = self.encoder.transform(imputed_cat)
            parts.append(encoded_cat)
            
        if not parts:
            return np.empty((len(df), 0))
            
        return np.hstack(parts)

    def fit_transform(self, df: pd.DataFrame) -> np.ndarray:
        """Convenience method to fit and transform in one step."""
        return self.fit(df).transform(df)

    def get_feature_names(self) -> List[str]:
        """Get output feature names corresponding to the columns of transformed arrays."""
        names = list(self.numeric_cols)
        if self.categorical_cols and hasattr(self.encoder, "get_feature_names_out"):
            encoded_names = self.encoder.get_feature_names_out(self.categorical_cols)
            names.extend(encoded_names)
        return names
