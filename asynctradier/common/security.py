from asynctradier.common import SecurityType


class Security:
    """
    Represents an ETB (Exchange Traded Bond) object.

    Attributes:
        symbol (str): The symbol of the ETB.
        description (str): The description of the ETB.
        type (ETBType): The type of the ETB.
        exchange (str): The exchange where the ETB is traded.
    """

    def __init__(self, **kargs):
        self.symbol = kargs.get("symbol", None)
        self.description = kargs.get("description", None)
        self.type = SecurityType(kargs.get("type", None)) if kargs.get("type") else None
        self.exchange = kargs.get("exchange", None)

    def to_dict(self):
        """
        Converts the ETB object to a dictionary.

        Returns:
            dict: A dictionary representation of the ETB object.
        """
        return {
            "symbol": self.symbol,
            "description": self.description,
            "type": self.type.value if self.type else None,
            "exchange": self.exchange,
        }

    def to_str(self):
        """
        Converts the ETB object to a string representation.

        Returns:
            str: A string representation of the ETB object.
        """
        return f"Security(symbol={self.symbol}, description={self.description}, type={self.type.value if self.type else None}, exchange={self.exchange})"

    def __repr__(self):
        """
        Returns a string representation of the ETB object.

        Returns:
            str: A string representation of the ETB object.
        """
        return self.to_str()
