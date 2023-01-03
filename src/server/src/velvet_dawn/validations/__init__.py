from typing import Union

from velvet_dawn import errors


def is_int(value: int, min=None, max=None, error_prefix: str = None):
    if not isinstance(value, int):
        raise errors.ValidationError(f"{error_prefix} must be an integer.")

    if min is not None and value < min:
        raise errors.ValidationError(f"{error_prefix} must greater than {min}.")

    if max is not None and value > max:
        raise errors.ValidationError(f"{error_prefix} must smaller than {max}.")


def is_number(value: Union[int, float], min=None, max=None, error_prefix: str = None):
    if not isinstance(value, int) and not isinstance(value, float):
        raise errors.ValidationError(f"{error_prefix} must be a number.")

    if min is not None and value < min:
        raise errors.ValidationError(f"{error_prefix} must greater than {min}.")

    if max is not None and value > max:
        raise errors.ValidationError(f"{error_prefix} must smaller than {max}.")


def is_bool(value: Union[bool], error_prefix: str = None):
    if not isinstance(value, bool):
        raise errors.ValidationError(f"{error_prefix} must be an boolean.")
