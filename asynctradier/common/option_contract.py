"""
This module defines the OptionContract class, which represents an option contract in a trading system.
"""

from asynctradier.common import OptionType, OrderSide
from asynctradier.exceptions import InvalidExiprationDate, InvalidOptionType
from asynctradier.utils.common import build_option_symbol, is_valid_expiration_date


class OptionContract:
    """
    Represents an option contract in a trading system.

    Attributes:
        symbol (str): The symbol of the option contract.
        expiration_date (str): The expiration date of the option contract.
        strike (float): The strike price of the option contract.
        option_type (str): The type of the option contract (e.g., 'call', 'put').
        order_side (OrderSide): The order side of the option contract (e.g., 'buy', 'sell').
        quantity (int): The quantity of the option contract.
    """

    def __init__(
        self,
        symbol: str,
        expiration_date: str,
        strike: float,
        option_type: OptionType,
        order_side: OrderSide,
        quantity: int,
    ) -> None:
        if not is_valid_expiration_date(expiration_date):
            raise InvalidExiprationDate(expiration_date)
        if not isinstance(option_type, OptionType):
            raise InvalidOptionType(option_type)

        self.symbol = symbol
        self.expiration_date = expiration_date
        self.strike = strike
        self.option_type = option_type
        self.order_side = order_side
        self.quantity = quantity

    def __str__(self) -> str:
        return f"{self.order_side.value} {build_option_symbol(self.symbol, self.expiration_date, self.strike, self.option_type)}"

    @property
    def option_symbol(self) -> str:
        """
        Returns the option symbol for the contract.

        The option symbol is built using the contract's symbol, expiration date,
        strike price, and option type.

        Returns:
            str: The option symbol.
        """
        return build_option_symbol(
            self.symbol, self.expiration_date, self.strike, self.option_type.value
        )
