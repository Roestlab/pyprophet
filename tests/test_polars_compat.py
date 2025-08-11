# encoding: utf-8
"""
Tests for polars compatibility utilities.
"""

import pandas as pd
import polars as pl
import numpy as np
import tempfile
import os
from pyprophet.util.compat import (
    to_polars,
    to_pandas,
    ensure_polars,
    ensure_pandas,
    compatible_read_csv,
    compatible_write_csv
)


def test_to_polars():
    """Test conversion from pandas to polars."""
    # Create test pandas DataFrame
    pd_df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': ['x', 'y', 'z'],
        'C': [1.1, 2.2, 3.3]
    })
    
    # Convert to polars
    pl_df = to_polars(pd_df)
    
    # Check types and content
    assert isinstance(pl_df, pl.DataFrame)
    assert pl_df.shape == (3, 3)
    assert pl_df.columns == ['A', 'B', 'C']
    assert pl_df.get_column('A').to_list() == [1, 2, 3]
    assert pl_df.get_column('B').to_list() == ['x', 'y', 'z']
    
    # Test with already polars DataFrame
    pl_df2 = to_polars(pl_df)
    assert isinstance(pl_df2, pl.DataFrame)
    assert pl_df2.frame_equal(pl_df)


def test_to_pandas():
    """Test conversion from polars to pandas."""
    # Create test polars DataFrame
    pl_df = pl.DataFrame({
        'A': [1, 2, 3],
        'B': ['x', 'y', 'z'],
        'C': [1.1, 2.2, 3.3]
    })
    
    # Convert to pandas
    pd_df = to_pandas(pl_df)
    
    # Check types and content
    assert isinstance(pd_df, pd.DataFrame)
    assert pd_df.shape == (3, 3)
    assert list(pd_df.columns) == ['A', 'B', 'C']
    assert list(pd_df['A']) == [1, 2, 3]
    assert list(pd_df['B']) == ['x', 'y', 'z']
    
    # Test with already pandas DataFrame
    pd_df2 = to_pandas(pd_df)
    assert isinstance(pd_df2, pd.DataFrame)
    assert pd_df2.equals(pd_df)


def test_ensure_functions():
    """Test ensure_polars and ensure_pandas functions."""
    # Test data
    pd_df = pd.DataFrame({'x': [1, 2, 3]})
    pl_df = pl.DataFrame({'x': [1, 2, 3]})
    
    # Test ensure_polars
    assert isinstance(ensure_polars(pd_df), pl.DataFrame)
    assert isinstance(ensure_polars(pl_df), pl.DataFrame)
    
    # Test ensure_pandas
    assert isinstance(ensure_pandas(pd_df), pd.DataFrame)
    assert isinstance(ensure_pandas(pl_df), pd.DataFrame)


def test_csv_compatibility():
    """Test CSV read/write compatibility."""
    # Create test data
    test_data = {
        'id': [1, 2, 3, 4],
        'score': [0.1, 0.5, 0.8, 0.9],
        'label': ['A', 'B', 'C', 'D']
    }
    
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = os.path.join(tmpdir, 'test.csv')
        
        # Create original DataFrame and write with polars
        pl_df = pl.DataFrame(test_data)
        compatible_write_csv(pl_df, csv_path)
        
        # Read back with polars
        pl_df_read = compatible_read_csv(csv_path, use_polars=True)
        assert isinstance(pl_df_read, pl.DataFrame)
        assert pl_df_read.shape == (4, 3)
        
        # Read back with pandas
        pd_df_read = compatible_read_csv(csv_path, use_polars=False)
        assert isinstance(pd_df_read, pd.DataFrame)
        assert pd_df_read.shape == (4, 3)
        
        # Test pandas write
        pd_df = pd.DataFrame(test_data)
        csv_path2 = os.path.join(tmpdir, 'test2.csv')
        compatible_write_csv(pd_df, csv_path2, index=False)
        
        # Verify file was created
        assert os.path.exists(csv_path2)


def test_error_handling():
    """Test error handling for invalid inputs."""
    try:
        to_polars("invalid")
        assert False, "Should have raised TypeError"
    except TypeError:
        pass
    
    try:
        to_pandas(123)
        assert False, "Should have raised TypeError"
    except TypeError:
        pass


if __name__ == "__main__":
    test_to_polars()
    test_to_pandas()
    test_ensure_functions()
    test_csv_compatibility()
    test_error_handling()
    print("All tests passed!")