"""

"""

import re

from asynctradier.exceptions import InvalidExiprationDate, InvalidOptionType


def build_option_symbol(
    symbol: str, expiration_date: str, strike: float, option_type: str
) -> str:
    """
    Build an option symbol based on the given parameters.

    Args:
        symbol (str): The underlying symbol.
        expiration_date (str): The expiration date of the option in the format "YYYY-MM-DD".
        strike (float): The strike price of the option.
        option_type (str): The type of the option, either "CALL" or "PUT".

    Returns:
        str: The option symbol.

    Raises:
        InvalidExiprationDate: If the expiration date is not in the valid format.
        InvalidOptionType: If the option type is not valid.
    """
    if not is_valid_expiration_date(expiration_date):
        raise InvalidExiprationDate(expiration_date)

    if not is_valid_option_type(option_type):
        raise InvalidOptionType(option_type)
    return f"{symbol.upper()}{expiration_date.replace('-', '')[2:]}{option_type.upper()[0]}{str(int(strike * 1000)).zfill(8)}"


def is_valid_expiration_date(expiration: str) -> bool:
    """
    Check if the given expiration date is in the valid format.

    Args:
        expiration (str): The expiration date to be checked.

    Returns:
        bool: True if the expiration date is valid, False otherwise.
    """
    # valid exp date is YYYY-MM-DD
    return bool(re.match(r"\d{4}-\d{2}-\d{2}", expiration))


def is_valid_option_type(option_type: str) -> bool:
    """
    Check if the given option type is valid.

    Args:
        option_type (str): The option type to be checked.

    Returns:
        bool: True if the option type is valid, False otherwise.
    """
    return option_type.upper() in ("CALL", "PUT")
