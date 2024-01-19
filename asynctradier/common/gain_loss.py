class ProfitLoss:
    """
    ProfitLoss class for storing profit/loss information for a security.

    Attributes:
        close_date (str): Date the position was closed
        cost (float): Total cost of the position
        gain_loss (float): Gain or loss on the position
        gain_loss_percent (float): Gain or loss represented as percent
        open_date (str): Date the position was opened
        proceeds (float): Total amount received for the position
        quantity (float): Quantity of shares/contracts
        symbol (str): Symbol of the security held
        term (int): Term in months position was held
    """

    def __init__(self, **kwargs):
        self.close_date = kwargs.get("close_date")
        self.cost = float(kwargs.get("cost")) if kwargs.get("cost") else 0.0
        self.gain_loss = (
            float(kwargs.get("gain_loss")) if kwargs.get("gain_loss") else 0.0
        )
        self.gain_loss_percent = (
            float(kwargs.get("gain_loss_percent"))
            if kwargs.get("gain_loss_percent")
            else 0.0
        )
        self.open_date = kwargs.get("open_date")
        self.proceeds = float(kwargs.get("proceeds")) if kwargs.get("proceeds") else 0.0
        self.quantity = float(kwargs.get("quantity")) if kwargs.get("quantity") else 0.0
        self.symbol = kwargs.get("symbol")
        self.term = int(kwargs.get("term")) if kwargs.get("term") else 0

    def to_dict(self):
        """
        Converts the ProfitLoss object to a dictionary.

        Returns:
            dict: A dictionary representation of the ProfitLoss object.
        """
        return {
            "close_date": self.close_date,
            "cost": self.cost,
            "gain_loss": self.gain_loss,
            "gain_loss_percent": self.gain_loss_percent,
            "open_date": self.open_date,
            "proceeds": self.proceeds,
            "quantity": self.quantity,
            "symbol": self.symbol,
            "term": self.term,
        }

    def __str__(self):
        return f"ProfitLoss(close_date={self.close_date}, cost={self.cost}, gain_loss={self.gain_loss}, gain_loss_percent={self.gain_loss_percent}, open_date={self.open_date}, proceeds={self.proceeds}, quantity={self.quantity}, symbol={self.symbol}, term={self.term})"
