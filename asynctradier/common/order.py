"""
This module defines the Order class, which represents an order in a trading system.
"""

from asynctradier.common import Duration, OrderClass, OrderSide, OrderStatus, OrderType


class Order:
    """
    Represent an Order object.

    Args:
        **kwargs: Additional keyword arguments representing the order attributes.

    Attributes:
        id (int): The ID of the order.
        type (OrderType): The type of the order.
        symbol (str): The symbol of the order.
        side (OrderSide): The side of the order.
        quantity (float): The quantity of the order.
        status (str): The status of the order.
        duration (Duration): The duration of the order.
        avg_fill_price (float): The average fill price of the order.
        exec_quantity (float): The executed quantity of the order.
        last_fill_price (float): The last fill price of the order.
        last_fill_quantity (float): The last fill quantity of the order.
        remaining_quantity (float): The remaining quantity of the order.
        create_date (str): The creation date of the order.
        transaction_date (str): The transaction date of the order.
        class_ (OrderClass): The class of the order.
        option_symbol (str): The option symbol of the order.
        price (float): The price of the order.
        number_of_legs (int): The number of legs of the order.
        legs (list[Order]): The legs of the order.
    """

    def __init__(
        self,
        **kwargs,
    ) -> None:
        assert kwargs.get("id", None) is not None
        self.id = kwargs["id"]
        self.type = OrderType(kwargs["type"]) if kwargs.get("type", None) else None
        self.symbol = kwargs.get("symbol", None)
        self.side = OrderSide(kwargs["side"]) if kwargs.get("side", None) else None
        self.quantity = kwargs.get("quantity", None)
        self.status = (
            OrderStatus(kwargs["status"]) if kwargs.get("status", None) else None
        )
        self.duration = (
            Duration(kwargs["duration"]) if kwargs.get("duration", None) else None
        )
        self.avg_fill_price = kwargs.get("avg_fill_price", None)
        self.exec_quantity = kwargs.get("exec_quantity", None)
        self.last_fill_price = kwargs.get("last_fill_price", None)
        self.last_fill_quantity = kwargs.get("last_fill_quantity", None)
        self.remaining_quantity = kwargs.get("remaining_quantity", None)
        self.create_date = kwargs.get("create_date", None)
        self.transaction_date = kwargs.get("transaction_date", None)
        self.class_ = OrderClass(kwargs["class"]) if kwargs.get("class", None) else None
        self.option_symbol = kwargs.get("option_symbol", None)
        self.price = kwargs.get("price", None)
        self.number_of_legs = kwargs.get("num_legs", None)
        self.legs = [Order(**leg) for leg in kwargs.get("leg", [])]

    def __str__(self) -> str:
        """
        Return a string representation of the Order object.

        Returns:
            str: A string representation of the Order object.
        """
        return (
            f"Order(id={self.id}, type={self.type}, symbol={self.symbol}, "
            f"side={self.side}, quantity={self.quantity}, status={self.status}, "
            f"duration={self.duration}, avg_fill_price={self.avg_fill_price}, "
            f"exec_quantity={self.exec_quantity}, last_fill_price={self.last_fill_price}, "
            f"last_fill_quantity={self.last_fill_quantity}, "
            f"remaining_quantity={self.remaining_quantity}, "
            f"create_date={self.create_date}, "
            f"transaction_date={self.transaction_date}, "
            f"class={self.class_}, option_symbol={self.option_symbol}, "
            f"price={self.price}, number_of_legs={self.number_of_legs}, "
            f"legs={self.legs})"
        )
