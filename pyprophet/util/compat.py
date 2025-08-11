"""
Compatibility utilities for pandas/polars interoperability.

This module provides helper functions to ensure smooth transitions between
pandas and polars DataFrames in the pyprophet codebase.
"""

import pandas as pd
import polars as pl
from typing import Union


def to_polars(df: Union[pd.DataFrame, pl.DataFrame]) -> pl.DataFrame:
    """
    Convert a pandas DataFrame to polars DataFrame.
    
    Args:
        df: Input DataFrame (pandas or polars)
        
    Returns:
        pl.DataFrame: Polars DataFrame
    """
    if isinstance(df, pd.DataFrame):
        return pl.from_pandas(df)
    elif isinstance(df, pl.DataFrame):
        return df
    else:
        raise TypeError(f"Expected pd.DataFrame or pl.DataFrame, got {type(df)}")


def to_pandas(df: Union[pd.DataFrame, pl.DataFrame]) -> pd.DataFrame:
    """
    Convert a polars DataFrame to pandas DataFrame.
    
    Args:
        df: Input DataFrame (pandas or polars)
        
    Returns:
        pd.DataFrame: Pandas DataFrame
    """
    if isinstance(df, pl.DataFrame):
        return df.to_pandas()
    elif isinstance(df, pd.DataFrame):
        return df
    else:
        raise TypeError(f"Expected pd.DataFrame or pl.DataFrame, got {type(df)}")


def ensure_polars(df: Union[pd.DataFrame, pl.DataFrame]) -> pl.DataFrame:
    """
    Ensure the input is a polars DataFrame.
    Alias for to_polars for clearer intent.
    """
    return to_polars(df)


def ensure_pandas(df: Union[pd.DataFrame, pl.DataFrame]) -> pd.DataFrame:
    """
    Ensure the input is a pandas DataFrame.
    Alias for to_pandas for clearer intent.
    """
    return to_pandas(df)


def compatible_read_csv(filepath: str, use_polars: bool = True, **kwargs) -> Union[pd.DataFrame, pl.DataFrame]:
    """
    Read CSV file using either pandas or polars.
    
    Args:
        filepath: Path to CSV file
        use_polars: If True, use polars; if False, use pandas
        **kwargs: Additional arguments passed to the read function
        
    Returns:
        DataFrame in the requested format
    """
    if use_polars:
        return pl.read_csv(filepath, **kwargs)
    else:
        return pd.read_csv(filepath, **kwargs)


def compatible_write_csv(df: Union[pd.DataFrame, pl.DataFrame], filepath: str, **kwargs) -> None:
    """
    Write DataFrame to CSV using the appropriate method.
    
    Args:
        df: Input DataFrame
        filepath: Output file path
        **kwargs: Additional arguments passed to the write function
    """
    if isinstance(df, pl.DataFrame):
        # Map pandas-style kwargs to polars equivalents
        polars_kwargs = {}
        if 'sep' in kwargs:
            polars_kwargs['separator'] = kwargs['sep']
            kwargs.pop('sep')
        if 'index' in kwargs:
            # Polars doesn't have index concept, remove this parameter
            kwargs.pop('index')
        polars_kwargs.update(kwargs)
        df.write_csv(filepath, **polars_kwargs)
    elif isinstance(df, pd.DataFrame):
        df.to_csv(filepath, **kwargs)
    else:
        raise TypeError(f"Expected pd.DataFrame or pl.DataFrame, got {type(df)}")