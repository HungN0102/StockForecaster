from datetime import timedelta, timezone, datetime

def validate_equation(equation_func, replacement=None):
    try:
        if equation_func == None:
            return replacement
        return equation_func()
    except (TypeError, ValueError, KeyError, ZeroDivisionError, AttributeError):
        return replacement
    
def nvl(*args):
    """
    Returns the first non-null argument passed to the function.
    If all arguments are None, it returns None.
    """
    for arg in args:
        if arg is not None:
            return arg
    return None

def trace(string):
    print(string)
    return string
    
def translate_insider_transaction(transactionCode, transactionPrice, isDerivative):
    # Handle Acquisition-type transactions
    if transactionCode == 'A':
        if isDerivative:
            # Typically represents an option exercise if a derivative transaction.
            return f"Option Exercise at price {transactionPrice:.2f} per share"
        else:
            if transactionPrice == 0:
                return "Stock Award (Grant) at price 0.00 per share"
            else:
                return f"Purchase at price {transactionPrice:.2f} per share"
    
    # Handle Sale / Disposition-type transactions
    elif transactionCode in ['D', 'S']:
        if isDerivative:
            return f"Option Disposition at price {transactionPrice:.2f} per share"
        else:
            return f"Sale at price {transactionPrice:.2f} per share"
    
    # Handle a direct purchase code
    elif transactionCode == 'P':
        return f"Purchase at price {transactionPrice:.2f} per share"
    
    # Handle option exercise if a distinct code is used (commonly 'M' for derivative exercise)
    elif transactionCode == 'M':
        return f"Option Exercise at price {transactionPrice:.2f} per share"
    
    # Unknown or unhandled transaction code
    else:
        return "Unknown transaction type"
    
def format_value(num, currency):
    sign = ""
    if num < 0:
        sign = "-"
    if abs(num) > 1000000:
        return f'{sign}{currency}{round(abs(num) / 1000000, 1)}M'
    return f'{sign}{currency}{round(abs(num) / 1000)}K'

def validate_model_insert(model, hours_ago):
    if model:
        # Get the current time in UTC
        now = datetime.now(timezone.utc)

        # Check if the last entry is older than 4 hours
        if now - model.created_at > timedelta(hours=hours_ago):
            return True  # More than hours_ago hours old
        else:
            return False  # Still fresh
    else:
        return True  # No entries exist, so it's "old" by default