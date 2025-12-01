# utils.py
def safe_float(value):
    try:
        return float(value)
    except:
        raise ValueError("Amount must be a valid number.")
