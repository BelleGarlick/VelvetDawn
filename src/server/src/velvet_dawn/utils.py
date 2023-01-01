bool_true_values = ["True", "true", "1"]


def parse_type(value: str, _type=None, default=None):
    if value is None: return default
    elif _type == str: return value
    elif _type == float: return float(value)
    elif _type == int: return int(value)
    elif _type == bool: return value in bool_true_values
    else:
        return value
