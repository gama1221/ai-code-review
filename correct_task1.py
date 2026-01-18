# Write your corrected implementation for Task 1 here.
# Do not modify `task1.py`.

def calculate_average_order_value(orders):
    """
    Calculate the average value of completed (non-cancelled) orders.
    
    Args:
        orders: List of order dictionaries, each containing at minimum:
                - "amount" (int or float): Order value
                - "status" (str): Order status
    
    Returns:
        float: Average order value for completed orders, or 0.0 if no completed orders exist
    
    Raises:
        TypeError: If orders is not a list
        ValueError: If orders structure is invalid
    """
    # Input validation
    if orders is None:
        raise TypeError("Orders cannot be None")
    
    if not isinstance(orders, list):
        raise TypeError(f"Expected list, got {type(orders).__name__}")
    
    # Handle empty orders
    if not orders:
        return 0.0
    
    total = 0.0
    completed_count = 0
    
    for i, order in enumerate (orders):
        # Validate order structure
        if not isinstance(order, dict):
            raise ValueError(f"Order at index {i} must be a dictionary, got {type(order).__name__}")
        
        if "status" not in order:
            raise ValueError(f"Order at index {i} missing 'status' key")
        
        if "amount" not in order:
            raise ValueError(f"Order at index {i} missing 'amount' key")
        
        # Validate amount type and value
        amount = order["amount"]
        if not isinstance(amount, (int, float)):
            raise ValueError(f"Order at index {i}: amount must be numeric, got {type(amount).__name__}")
        
        if amount < 0:
            # Handle negative amounts (refunds) based on business logic
            # Could log a warning or handle differently
            pass
        
        # Process only completed (non-cancelled) orders
        if order["status"] != "cancelled":
            total += float(amount)
            completed_count += 1
    
    # Return average only for completed orders
    if completed_count == 0:
        return 0.0
    
    # Use Decimal for monetary calculations if high precision needed
    return total / completed_count


# Try with this values

# orders = [
#     {"status": "completed", "amount": 100},
#     {"status": "cancelled", "amount": 200},
#     {"status": "completed", "amount": 100}
# ]

# print("Average : ", calculate_average_order_value(orders))