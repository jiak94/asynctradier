from asynctradier.common import AccountType


class CashAccountBalanceDetails:
    """
    Represents the details of a cash account balance.

    Attributes:
        cash_available (float): The amount of cash available in the account.
        sweep (float): The amount of cash swept from the account.
        unsettled_funds (float): The amount of funds that are currently unsettled.
    """

    def __init__(self, **kwargs):
        self.cash_available = kwargs.get("cash_available", 0.0)
        self.sweep = kwargs.get("sweep", 0.0)
        self.unsettled_funds = kwargs.get("unsettled_funds", 0.0)

    def to_dict(self):
        """
        Converts the AccountBalance object to a dictionary.

        Returns:
            dict: A dictionary representation of the AccountBalance object.
        """
        return {
            "cash_available": self.cash_available,
            "sweep": self.sweep,
            "unsettled_funds": self.unsettled_funds,
        }

    def __str__(self):
        return f"CashAccountBalanceDetails(capacity={self.cash_available}, sweep={self.sweep}, unsettled_funds={self.unsettled_funds})"


class MarginAccountBalanceDetails:
    """
    Represents the details of a margin account balance.

    Attributes:
        fed_call (float): The federal call amount.
        maintenance_call (float): The maintenance call amount.
        option_buying_power (float): The buying power for options.
        stock_buying_power (float): The buying power for stocks.
        stock_short_value (float): The value of shorted stocks.
        sweep (float): The sweep amount.
    """

    def __init__(self, **kwargs):
        self.fed_call = kwargs.get("fed_call", 0.0)
        self.maintenance_call = kwargs.get("maintenance_call", 0.0)
        self.option_buying_power = kwargs.get("option_buying_power", 0.0)
        self.stock_buying_power = kwargs.get("stock_buying_power", 0.0)
        self.stock_short_value = kwargs.get("stock_short_value", 0.0)
        self.sweep = kwargs.get("sweep", 0.0)

    def to_dict(self):
        """
        Converts the AccountBalance object to a dictionary.

        Returns:
            dict: A dictionary representation of the AccountBalance object.
        """
        return {
            "fed_call": self.fed_call,
            "maintenance_call": self.maintenance_call,
            "option_buying_power": self.option_buying_power,
            "stock_buying_power": self.stock_buying_power,
            "stock_short_value": self.stock_short_value,
            "sweep": self.sweep,
        }

    def __str__(self):
        return f"MarginAccountBalanceDetails(fed_call={self.fed_call}, maintenance_call={self.maintenance_call}, option_buying_power={self.option_buying_power}, stock_buying_power={self.stock_buying_power}, stock_short_value={self.stock_short_value}, sweep={self.sweep})"


class PDTAccountBalanceDetails:
    """
    Represents the account balance details for a Pattern Day Trader (PDT).

    Attributes:
        fed_call (float): The amount of the Federal Call.
        maintenance_call (float): The amount of the Maintenance Call.
        option_buying_power (float): The buying power for options trading.
        stock_buying_power (float): The buying power for stock trading.
        stock_short_value (float): The value of shorted stocks.
    """

    def __init__(self, **kwargs):
        self.fed_call = kwargs.get("fed_call", 0.0)
        self.maintenance_call = kwargs.get("maintenance_call", 0.0)
        self.option_buying_power = kwargs.get("option_buying_power", 0.0)
        self.stock_buying_power = kwargs.get("stock_buying_power", 0.0)
        self.stock_short_value = kwargs.get("stock_short_value", 0.0)

    def to_dict(self):
        """
        Converts the AccountBalance object to a dictionary.

        Returns:
            dict: A dictionary representation of the AccountBalance object.
        """
        return {
            "fed_call": self.fed_call,
            "maintenance_call": self.maintenance_call,
            "option_buying_power": self.option_buying_power,
            "stock_buying_power": self.stock_buying_power,
            "stock_short_value": self.stock_short_value,
        }

    def __str__(self):
        return f"PDTAccountBalanceDetails(fed_call={self.fed_call}, maintenance_call={self.maintenance_call}, option_buying_power={self.option_buying_power}, stock_buying_power={self.stock_buying_power}, stock_short_value={self.stock_short_value})"


class AccountBalance:
    """
    Represents the balance of an account.

    Attributes:
        option_short_value (float): The short value of options in the account.
        total_equity (float): The total equity of the account.
        account_number (str): The account number.
        account_type (AccountType): The type of the account.
        close_pl (float): The close profit/loss of the account.
        current_requirement (float): The current requirement of the account.
        equity (float): The equity of the account.
        long_market_value (float): The long market value of the account.
        market_value (float): The market value of the account.
        open_pl (float): The open profit/loss of the account.
        option_long_value (float): The long value of options in the account.
        option_requirement (float): The option requirement of the account.
        pending_orders_count (int): The count of pending orders in the account.
        short_market_value (float): The short market value of the account.
        stock_long_value (float): The long value of stocks in the account.
        total_cash (float): The total cash in the account.
        uncleared_funds (float): The uncleared funds in the account.
        pending_cash (float): The pending cash in the account.
        cash (CashAccountBalanceDetails): The details of the cash account balance (if account type is cash).
        margin (MarginAccountBalanceDetails): The details of the margin account balance (if account type is margin).
        pdt (PDTAccountBalanceDetails): The details of the PDT account balance (if account type is pdt).
    """

    def __init__(self, **kwargs):
        self.option_short_value = kwargs.get("option_short_value")
        self.total_equity = kwargs.get("total_equity")
        self.account_number = kwargs.get("account_number")
        self.account_type = (
            AccountType(kwargs.get("account_type"))
            if kwargs.get("account_type")
            else None
        )
        self.close_pl = kwargs.get("close_pl")
        self.current_requirement = kwargs.get("current_requirement")
        self.equity = kwargs.get("equity")
        self.long_market_value = kwargs.get("long_market_value")
        self.market_value = kwargs.get("market_value")
        self.open_pl = kwargs.get("open_pl")
        self.option_long_value = kwargs.get("option_long_value")
        self.option_requirement = kwargs.get("option_requirement")
        self.pending_orders_count = kwargs.get("pending_orders_count")
        self.short_market_value = kwargs.get("short_market_value")
        self.stock_long_value = kwargs.get("stock_long_value")
        self.total_cash = kwargs.get("total_cash")
        self.uncleared_funds = kwargs.get("uncleared_funds")
        self.pending_cash = kwargs.get("pending_cash")

        self.cash = (
            CashAccountBalanceDetails(**kwargs.get("cash"))
            if kwargs.get("cash")
            else None
        )
        self.margin = (
            MarginAccountBalanceDetails(**kwargs.get("margin"))
            if kwargs.get("margin")
            else None
        )
        self.pdt = (
            PDTAccountBalanceDetails(**kwargs.get("pdt")) if kwargs.get("pdt") else None
        )

    def to_dict(self):
        """
        Converts the AccountBalance object to a dictionary.

        Returns:
            dict: A dictionary representation of the AccountBalance object.
        """
        return {
            "option_short_value": self.option_short_value,
            "total_equity": self.total_equity,
            "account_number": self.account_number,
            "account_type": self.account_type,
            "close_pl": self.close_pl,
            "current_requirement": self.current_requirement,
            "equity": self.equity,
            "long_market_value": self.long_market_value,
            "market_value": self.market_value,
            "open_pl": self.open_pl,
            "option_long_value": self.option_long_value,
            "option_requirement": self.option_requirement,
            "pending_orders_count": self.pending_orders_count,
            "short_market_value": self.short_market_value,
            "stock_long_value": self.stock_long_value,
            "total_cash": self.total_cash,
            "uncleared_funds": self.uncleared_funds,
            "pending_cash": self.pending_cash,
            "cash": self.cash.to_dict() if self.cash else None,
            "margin": self.margin.to_dict() if self.margin else None,
            "pdt": self.pdt.to_dict() if self.pdt else None,
        }
