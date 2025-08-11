# PyProphet Pandas to Polars Migration

## Overview

This document summarizes the migration of PyProphet from pandas to polars for improved performance and efficiency. Polars is a fast DataFrame library implemented in Rust that provides significant performance improvements over pandas for many data processing tasks.

## Modules Converted

### Core Foundation Modules (✅ Complete)

1. **pyprophet/io/_base.py** (21 pandas usages)
   - Abstract base classes for data readers and writers
   - DataFrame type hints updated from `pd.DataFrame` to `pl.DataFrame`
   - CSV read/write operations converted to polars equivalents
   - Complex aggregation and pivot operations converted
   - Normalization methods rewritten for polars

2. **pyprophet/scoring/data_handling.py** (8 pandas usages)
   - Core data processing for semi-supervised scoring
   - Experiment class updated for polars DataFrames
   - Data validation and cleanup functions converted
   - Feature scaling and ranking operations updated
   - Cross-validation splitting logic converted

3. **pyprophet/report.py** (5 pandas usages)
   - Reporting and visualization functionality
   - Matrix creation for run similarity analysis
   - Summary table generation for logging
   - PDF report data structures

4. **pyprophet/stats.py** (4 pandas usages)
   - Statistical analysis and metrics calculation
   - Error statistics DataFrame creation
   - Sensitivity value calculations
   - Compatibility with existing numpy/scipy workflows

5. **pyprophet/split.py** (1 pandas usage)
   - File splitting functionality
   - SQL query result handling with pandas→polars conversion bridge

### Utility Modules (✅ Complete)

6. **pyprophet/util/compat.py** (New)
   - Compatibility utilities for pandas/polars interoperability
   - Conversion functions between pandas and polars
   - Compatible CSV read/write functions
   - Error handling for type mismatches

## Key Changes Made

### DataFrame Operations

| Pandas | Polars | Notes |
|--------|--------|-------|
| `df[columns]` | `df.select(columns)` | Column selection |
| `df.rename(columns={...})` | `df.rename({...})` | Column renaming |
| `df[condition]` | `df.filter(condition)` | Row filtering |
| `df.groupby(...).apply(...)` | `df.group_by(...).agg(...)` | Grouping operations |
| `df.iloc[...]` | `df.slice(...)` or select by index | Positional indexing |
| `df.loc[...]` | `df.filter(...)` or `df.with_columns(...)` | Label-based indexing |
| `df.values` | `df.to_numpy()` | Array conversion |
| `pd.concat([...])` | `pl.concat([...])` | DataFrame concatenation |
| `df.pivot_table(...)` | `df.pivot(...)` | Pivot operations |

### Data Access

| Pandas | Polars | Notes |
|--------|--------|-------|
| `df.column_name` | `df.get_column("column_name")` | Column access |
| `df["column"]` | `df.get_column("column")` | Column access |
| `series.values` | `series.to_numpy()` | Series to array |
| `df.shape[0]` | `len(df)` | Row count |
| `df.columns` | `df.columns` | Column names (same) |

### Null/Missing Value Handling

| Pandas | Polars | Notes |
|--------|--------|-------|
| `pd.isnull(df)` | `df.is_null()` | Null detection |
| `df.dropna()` | `df.drop_nulls()` | Remove null values |
| `df.fillna(value)` | `df.fill_null(value)` | Fill null values |

### File I/O

| Pandas | Polars | Notes |
|--------|--------|-------|
| `pd.read_csv(file)` | `pl.read_csv(file)` | CSV reading |
| `df.to_csv(file, index=False)` | `df.write_csv(file)` | CSV writing |
| `sep` parameter | `separator` parameter | CSV delimiter |

## Performance Benefits

Polars provides several performance advantages over pandas:

1. **Memory Efficiency**: Lower memory usage due to optimized data structures
2. **Parallel Processing**: Automatic parallelization of operations
3. **Lazy Evaluation**: Query optimization through lazy evaluation
4. **Type Safety**: Stronger type system reduces runtime errors
5. **Zero-Copy Operations**: Reduced memory copying for better performance

## Backward Compatibility

### Compatibility Layer

The `pyprophet.util.compat` module provides utilities for smooth transitions:

- `to_polars()`: Convert pandas DataFrame to polars
- `to_pandas()`: Convert polars DataFrame to pandas
- `compatible_read_csv()`: Read CSV with either pandas or polars
- `compatible_write_csv()`: Write CSV from either DataFrame type

### External Dependencies

Some external libraries (e.g., scikit-learn) still require pandas DataFrames. In these cases:

1. Convert polars → pandas for external library calls
2. Process with external library
3. Convert back to polars for internal operations

Example in `_quantile_normalize()`:
```python
# Convert to pandas for scikit-learn compatibility
pandas_matrix = matrix.to_pandas()
normalized = quantile_transform(pandas_matrix.T, copy=True).T
# Convert back to polars
normalized_df = pl.from_pandas(pd.DataFrame(normalized, ...))
```

## Testing

### New Tests

- `tests/test_polars_compat.py`: Tests for compatibility utilities
- Validates conversion functions work correctly
- Tests CSV read/write compatibility
- Error handling verification

### Existing Tests

All existing tests should continue to work as the public APIs remain the same. The underlying DataFrame implementation has changed, but the external interface is preserved.

## Migration Benefits

1. **Performance**: Significant speed improvements for large datasets
2. **Memory**: Reduced memory usage for data processing
3. **Maintainability**: Cleaner, more explicit code
4. **Future-proofing**: Modern DataFrame library with active development
5. **Type Safety**: Better type checking and error detection

## Remaining Work

The following modules still contain pandas usage and could be converted in future updates:

- Export modules (`pyprophet/export/`)
- Glyco modules (`pyprophet/glyco/`)
- IPF modules (`pyprophet/ipf.py`)
- Various IO modules (`pyprophet/io/`)

However, the core functionality has been successfully migrated to polars, providing immediate performance benefits for the most critical data processing operations.

## Usage Example

```python
import polars as pl
from pyprophet.scoring.data_handling import Experiment
from pyprophet.util.compat import to_polars, to_pandas

# Create sample data
data = pl.DataFrame({
    'tg_id': [1, 1, 2, 2],
    'is_decoy': [False, True, False, True],
    'main_score': [0.8, 0.3, 0.9, 0.1]
})

# Use with Experiment class
exp = Experiment(data)
decoys = exp.get_decoy_peaks()
targets = exp.get_target_peaks()

# Convert to pandas if needed for external libraries
pandas_data = to_pandas(data)
# Process with external library...
# Convert back to polars
polars_result = to_polars(result)
```