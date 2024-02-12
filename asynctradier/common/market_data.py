from asynctradier.common import MarketDataType


class MarketData:
    """
    Represents market data for a specific type.

    Args:
        **kwargs: Additional keyword arguments to initialize the market data.

    Attributes:
        type (MarketDataType): The type of market data.
        data (MarketDataTrade, MarketDataQuote, MarketDataSummary, MarketDataTimesale): The specific market data object based on the type.
    """

    def __init__(self, **kwargs):
        self.type = MarketDataType(kwargs.get("type"))
        if self.type in [MarketDataType.trade, MarketDataType.tradex]:
            self.data = MarketDataTrade(**kwargs)
        elif self.type == MarketDataType.quote:
            self.data = MarketDataQuote(**kwargs)
        elif self.type == MarketDataType.summary:
            self.data = MarketDataSummary(**kwargs)
        elif self.type == MarketDataType.timesale:
            self.data = MarketDataTimesale(**kwargs)

    def to_string(self) -> str:
        """
        Convert the MarketData object to a string representation.

        Returns:
            str: The string representation of the MarketData object.
        """
        return f"MarketData(type={self.type}, data={self.data})"

    def to_dict(self) -> dict:
        """
        Convert the MarketData object to a dictionary.

        Returns:
            dict: A dictionary representation of the MarketData object.
        """
        return {"type": self.type, "data": self.data.to_dict()}

    def __repr__(self) -> str:
        return self.to_string()


class MarketDataQuote:
    """
    Represents a market data quote.
    The quote event is issued when a viable quote has been created an exchange. This represents the most current bid/ask pricing available.

    Attributes:
        symbol (str): The symbol of the quote.
        bid (float): The bid price of the quote.
        bidsz (int): The bid size of the quote.
        bidexch (str): The exchange where the bid was placed.
        biddate (str): The date of the bid.
        ask (float): The ask price of the quote.
        asksz (int): The ask size of the quote.
        askexch (str): The exchange where the ask was placed.
        askdate (str): The date of the ask.
    """

    def __init__(self, **kwargs):
        self.symbol = kwargs.get("symbol")
        self.bid = kwargs.get("bid")
        self.bidsz = kwargs.get("bidsz")
        self.bidexch = kwargs.get("bidexch")
        self.biddate = kwargs.get("biddate")
        self.ask = kwargs.get("ask")
        self.asksz = kwargs.get("asksz")
        self.askexch = kwargs.get("askexch")
        self.askdate = kwargs.get("askdate")

    def to_string(self):
        """
        Convert the MarketDataQuote object to a string representation.

        Returns:
            str: A string representation of the MarketDataQuote object.
        """
        return f"MarketDataQuote(symbol={self.symbol}, bid={self.bid}, ask={self.ask})"

    def to_dict(self):
        """
        Convert the MarketData object to a dictionary.

        Returns:
            dict: A dictionary representation of the MarketData object.
        """
        return {
            "symbol": self.symbol,
            "bid": self.bid,
            "bidsz": self.bidsz,
            "bidexch": self.bidexch,
            "biddate": self.biddate,
            "ask": self.ask,
            "asksz": self.asksz,
            "askexch": self.askexch,
            "askdate": self.askdate,
        }

    def __repr__(self) -> str:
        return self.to_string()


class MarketDataTrade:
    """
    Represents a market data trade.
    The trade event is sent for all trade events at exchanges. By default, the trade event is filtered to only include valid ticks (removing trade corrections, errors, etc).

    Attributes:
        symbol (str): The symbol of the trade.
        exch (str): The exchange where the trade occurred.
        price (float): The price of the trade.
        size (int): The size of the trade.
        cvol (int): The cumulative volume of the trade.
        date (str): The date of the trade.
        last (str): The last price of the trade.
    """

    def __init__(self, **kwargs):
        self.symbol = kwargs.get("symbol")
        self.exch = kwargs.get("exch")
        self.price = kwargs.get("price")
        self.size = kwargs.get("size")
        self.cvol = kwargs.get("cvol")
        self.date = kwargs.get("date")
        self.last = kwargs.get("last")

    def to_string(self):
        """
        Convert the MarketDataTrade object to a string representation.

        Returns:
            str: A string representation of the MarketDataTrade object.
        """
        return f"MarketDataTrade(symbol={self.symbol}, price={self.price}, size={self.size})"

    def to_dict(self):
        """
        Convert the MarketData object to a dictionary.

        Returns:
            dict: A dictionary representation of the MarketData object.
        """
        return {
            "symbol": self.symbol,
            "exch": self.exch,
            "price": self.price,
            "size": self.size,
            "cvol": self.cvol,
            "date": self.date,
            "last": self.last,
        }

    def __repr__(self) -> str:
        return self.to_string()


class MarketDataSummary:
    """
    Represents a market data summary.
    The summary event is triggered when a market session high, low, open, or close event is triggered.

    Attributes:
        symbol (str): The symbol of the summary.
        exch (str): The exchange where the summary occurred.
        open (float): The opening price of the summary.
        high (float): The highest price of the summary.
        low (float): The lowest price of the summary.
        prev_close (float): The previous closing price of the summary.
    """

    def __init__(self, **kwargs):
        self.symbol = kwargs.get("symbol")
        self.open = kwargs.get("open")
        self.high = kwargs.get("high")
        self.low = kwargs.get("low")
        self.prev_close = kwargs.get("prevClose")

    def to_string(self):
        """
        Convert the MarketDataSummary object to a string representation.

        Returns:
            str: A string representation of the MarketDataSummary object.
        """
        return f"MarketDataSummary(symbol={self.symbol}, open={self.open}, high={self.high}, low={self.low})"

    def to_dict(self):
        """
        Convert the MarketData object to a dictionary.

        Returns:
            dict: A dictionary representation of the MarketData object.
        """
        return {
            "symbol": self.symbol,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "prev_close": self.prev_close,
        }

    def __repr__(self) -> str:
        return self.to_string()


class MarketDataTimesale:
    """
    Represents a market data timesale.
    Time and Sale represents a trade or other market event with price, like market open/close price, etc. Time and Sales are intended to provide information about trades in a continuous time slice (unlike Trade events which are supposed to provide snapshot about the current last trade). Timesale events are uniquely sequenced.

    Attributes:
        symbol (str): The symbol of the timesale.
        exch (str): The exchange of the timesale.
        bid (float): The bid price of the timesale.
        ask (float): The ask price of the timesale.
        last (float): The last price of the timesale.
        size (int): The size of the timesale.
        date (str): The date of the timesale.
        seq (int): The sequence number of the timesale.
        flag (str): The flag of the timesale. Reference: https://docs.dxfeed.com/misc/dxFeed_TimeAndSale_Sale_Conditions.htm
        cancel (bool): Indicates if the timesale is a cancel.
        correction (bool): Indicates if the timesale is a correction.
        session (str): The session of the timesale.
    """

    def __init__(self, **kwargs):
        self.symbol = kwargs.get("symbol")
        self.exch = kwargs.get("exch")
        self.bid = kwargs.get("bid")
        self.ask = kwargs.get("ask")
        self.last = kwargs.get("last")
        self.size = kwargs.get("size")
        self.date = kwargs.get("date")
        self.seq = kwargs.get("seq")
        self.flag = kwargs.get("flag")
        self.cancel = kwargs.get("cancel")
        self.correction = kwargs.get("correction")
        self.session = kwargs.get("session")

    def to_string(self):
        """
        Convert the MarketDataTimesale object to a string representation.

        Returns:
            str: A string representation of the MarketDataTimesale object.
        """
        return f"MarketDataTimesale(symbol={self.symbol}, last={self.last}, size={self.size})"

    def to_dict(self):
        """
        Convert the MarketDataTimesale object to a dictionary.

        Returns:
            dict: A dictionary representation of the MarketDataTimesale object.
        """
        return {
            "symbol": self.symbol,
            "exch": self.exch,
            "bid": self.bid,
            "ask": self.ask,
            "last": self.last,
            "size": self.size,
            "date": self.date,
            "seq": self.seq,
            "flag": self.flag,
            "cancel": self.cancel,
            "correction": self.correction,
            "session": self.session,
        }

    def __repr__(self) -> str:
        return self.to_string()
