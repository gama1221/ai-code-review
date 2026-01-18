# Write your corrected implementation for Task 3 here.
# Do not modify `task3.py`.

from typing import List, Union, Optional, Any
import numbers
import warnings
import math

def average_valid_measurements(
    values: List[Optional[Any]],
    *,
    strict_numeric: bool = False,
    allow_string_conversion: bool = True,
    handle_inf_nan: bool = False,
    min_valid_count: int = 1
) -> Optional[float]:
    """
    Calculate the average of valid numeric measurements, ignoring None values.
    
    Args:
        values: List of measurements (may include None or non-numeric values)
        strict_numeric: If True, only accepts int/float; if False, attempts conversion
        allow_string_conversion: If True, tries to convert numeric strings to float
        handle_inf_nan: If True, includes infinity and NaN as valid (dangerous for stats)
        min_valid_count: Minimum number of valid values required to return average
    
    Returns:
        Optional[float]: Average of valid measurements, or None if insufficient valid data
    
    Raises:
        TypeError: If values is not a list
        ValueError: If values contain non-convertible data (when strict_numeric=False)
    """
    # Input validation
    if not isinstance(values, list):
        raise TypeError(f"Expected list, got {type(values).__name__}")
    
    # Handle empty list
    if not values:
        warnings.warn(
            "Empty measurement list provided, returning None",
            UserWarning,
            stacklevel=2
        )
        return None
    
    total = 0.0
    valid_count = 0
    invalid_indices = []
    
    for i, value in enumerate(values):
        # Handle None values (skip them)
        if value is None:
            continue
        
        # Try to process as numeric value
        try:
            if isinstance(value, numbers.Number):
                # Handle special float values
                if not handle_inf_nan:
                    if math.isinf(value):
                        warnings.warn(
                            f"Infinite value at index {i}, skipping",
                            UserWarning,
                            stacklevel=2
                        )
                        invalid_indices.append((i, "infinity"))
                        continue
                    if math.isnan(value):
                        warnings.warn(
                            f"NaN value at index {i}, skipping",
                            UserWarning,
                            stacklevel=2
                        )
                        invalid_indices.append((i, "nan"))
                        continue
                
                numeric_value = float(value)
            
            elif allow_string_conversion and isinstance(value, str):
                # Attempt to convert string to float
                numeric_value = float(value)
                
                # Check for infinity/nan in strings
                if not handle_inf_nan:
                    if math.isinf(numeric_value):
                        warnings.warn(
                            f"Infinite value from string at index {i}, skipping",
                            UserWarning,
                            stacklevel=2
                        )
                        invalid_indices.append((i, "infinity_string"))
                        continue
                    if math.isnan(numeric_value):
                        warnings.warn(
                            f"NaN value from string at index {i}, skipping",
                            UserWarning,
                            stacklevel=2
                        )
                        invalid_indices.append((i, "nan_string"))
                        continue
            
            else:
                if strict_numeric:
                    raise ValueError(
                        f"Non-numeric value at index {i}: {repr(value)} "
                        f"(type: {type(value).__name__})"
                    )
                else:
                    # Try general conversion
                    numeric_value = float(value)
            
            # Successfully converted to numeric value
            total += numeric_value
            valid_count += 1
            
        except (ValueError, TypeError) as e:
            if strict_numeric:
                raise ValueError(
                    f"Non-convertible value at index {i}: {repr(value)} "
                    f"(error: {str(e)})"
                )
            else:
                warnings.warn(
                    f"Skipping non-convertible value at index {i}: {repr(value)}",
                    UserWarning,
                    stacklevel=2
                )
                invalid_indices.append((i, type(value).__name__))
    
    # Check if we have enough valid measurements
    if valid_count < min_valid_count:
        warnings.warn(
            f"Insufficient valid measurements: {valid_count} "
            f"(minimum required: {min_valid_count})",
            UserWarning,
            stacklevel=2
        )
        return None
    
    # Handle edge case where valid_count is 0 (should be caught by min_valid_count)
    if valid_count == 0:
        return None
    
    # Calculate average
    average = total / valid_count
    
    # Optional: Log statistics for debugging
    if invalid_indices:
        warnings.warn(
            f"Skipped {len(invalid_indices)} invalid measurements out of {len(values)} total",
            UserWarning,
            stacklevel=2
        )
    
    return average

# Try with this values
# values = [20, "20", 30]
# print(average_valid_measurements(values))