class Position:
    """
    Represents a trading position.

    Attributes:
        symbol (str): The symbol of the position.
        quantity (int): The quantity of shares held in the position.
        cost_basis (float): The average cost basis of the position.
        date_acquired (str): The date when the position was acquired.
    """

    def __init__(self, **kwargs) -> None:
        self.symbol = kwargs.get("symbol", None)
        self.quantity = kwargs.get("quantity", None)
        self.cost_basis = kwargs.get("cost_basis", None)
        self.date_acquired = kwargs.get("date_acquired", None)

    def __str__(self) -> str:
        return (
            f"Position(symbol={self.symbol}, quantity={self.quantity}, "
            f"cost_basis={self.cost_basis}, date_acquired={self.date_acquired})"
        )
