from asynctradier.common import Duration, OptionOrderSide, OrderClass, OrderType

"""
example:
{
    "id": 228749,
    "type": "market",
    "symbol": "SPY",
    "side": "buy_to_open",
    "quantity": 1.00000000,
    "status": "expired",
    "duration": "pre",
    "avg_fill_price": 0.00000000,
    "exec_quantity": 0.00000000,
    "last_fill_price": 0.00000000,
    "last_fill_quantity": 0.00000000,
    "remaining_quantity": 0.00000000,
    "create_date": "2018-06-06T20:16:17.342Z",
    "transaction_date": "2018-06-06T20:16:17.357Z",
    "class": "option",
    "option_symbol": "SPY180720C00274000"
},
"""


class Order:
    def __init__(
        self,
        id: int,
        **kwargs,
    ) -> None:
        self.id = id
        self.type = OrderType(kwargs["type"]) if kwargs.get("type", None) else None
        self.symbol = kwargs.get("symbol", None)
        self.side = (
            OptionOrderSide(kwargs["side"]) if kwargs.get("side", None) else None
        )
        self.quantity = kwargs.get("quantity", None)
        self.status = kwargs.get("status", None)
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

    def __str__(self) -> str:
        return (
            f"Order(id={self.id}, type={self.type}, symbol={self.symbol}, "
            f"side={self.side}, quantity={self.quantity}, status={self.status}, "
            f"duration={self.duration}, avg_fill_price={self.avg_fill_price}, "
            f"exec_quantity={self.exec_quantity}, last_fill_price={self.last_fill_price}, "
            f"last_fill_quantity={self.last_fill_quantity}, "
            f"remaining_quantity={self.remaining_quantity}, "
            f"create_date={self.create_date}, "
            f"transaction_date={self.transaction_date}, class={self.class_}, "
            f"option_symbol={self.option_symbol})"
        )
