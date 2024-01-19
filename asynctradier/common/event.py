from asynctradier.common import EventType, TradeType


class Event:
    """
    Represents an event.

    Attributes:
        amount (float): The amount of the event.
        date (str): The date of the event.
        type (EventType): The type of the event.
        description (str): The description of the event.
        commision (float): The commission of the event.
        price (float): The price of the event.
        quantity (float): The quantity of the event.
        symbol (str): The symbol of the event.
        trade_type (TradeType): The type of trade.
    """

    def __init__(self, **kwargs):
        self.amount = float(kwargs.get("amount")) if kwargs.get("amount") else 0.0
        self.date = kwargs.get("date")
        self.type = EventType(kwargs.get("type")) if kwargs.get("type") else None

        detail = kwargs.get(self.type.value, {})

        self.description = detail.get("description")
        self.commision = (
            float(detail.get("commision")) if detail.get("commision") else 0.0
        )
        self.price = float(detail.get("price")) if detail.get("price") else 0.0
        self.quantity = float(detail.get("quantity")) if detail.get("quantity") else 0.0
        self.symbol = detail.get("symbol")
        self.trade_type = (
            TradeType(detail.get("trade_type").lower())
            if detail.get("trade_type")
            else None
        )

    def to_dict(self):
        """
        Converts the Event object to a dictionary.

        Returns:
            dict: A dictionary representation of the Event object.
        """
        return {
            "amount": self.amount,
            "date": self.date,
            "type": self.type.value,
            "description": self.description,
            "commision": self.commision,
            "price": self.price,
            "symbol": self.symbol,
            "trade_type": self.trade_type.value,
            "quantity": self.quantity,
        }

    def __str__(self):
        return f"Event(amount={self.amount}, date={self.date}, type={self.type}, description={self.description}, commision={self.commision}, price={self.price}, symbol={self.symbol}, trade_type={self.trade_type})"
