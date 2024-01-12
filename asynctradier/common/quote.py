from asynctradier.common import OptionType, QuoteType


class Greeks:
    """
    Represents the Greeks of an option contract.

    Attributes:
        delta (float): The delta value of the option.
        gamma (float): The gamma value of the option.
        theta (float): The theta value of the option.
        vega (float): The vega value of the option.
        rho (float): The rho value of the option.
        phi (float): The phi value of the option.
        bid_iv (float): The bid implied volatility of the option.
        mid_iv (float): The mid implied volatility of the option.
        ask_iv (float): The ask implied volatility of the option.
        smv_vol (float): The smoothed volatility of the option.
        updated_at (str): The timestamp when the Greeks were last updated.
    """

    def __init__(self, **kwargs):
        self.delta = kwargs.get("delta")
        self.gamma = kwargs.get("gamma")
        self.theta = kwargs.get("theta")
        self.vega = kwargs.get("vega")
        self.rho = kwargs.get("rho")
        self.phi = kwargs.get("phi")
        self.bid_iv = kwargs.get("bid_iv")
        self.mid_iv = kwargs.get("mid_iv")
        self.ask_iv = kwargs.get("ask_iv")
        self.smv_vol = kwargs.get("smv_vol")
        self.updated_at = kwargs.get("updated_at")


class Quote:
    """
    Represents a quote for a financial instrument.

    Attributes:
        symbol (str): The symbol of the financial instrument.
        description (str): The description of the financial instrument.
        exch (str): The exchange where the financial instrument is traded.
        type (QuoteType): The type of the quote.
        last (float): The last price of the financial instrument.
        change (float): The change in price of the financial instrument.
        volume (int): The volume of the financial instrument.
        open (float): The opening price of the financial instrument.
        high (float): The highest price of the financial instrument.
        low (float): The lowest price of the financial instrument.
        close (float): The closing price of the financial instrument.
        bid (float): The bid price of the financial instrument.
        ask (float): The ask price of the financial instrument.
        underlying (str, optional): The underlying symbol for options.
        strike (float, optional): The strike price for options.
        change_percentage (float): The percentage change in price of the financial instrument.
        average_volume (int): The 90-day average volume of the financial instrument.
        last_volume (int): The volume of the last price of the financial instrument.
        trade_date (str): The most recent trade date of the financial instrument.
        prevclose (float): The previous closing price of the financial instrument.
        week_52_high (float): The 52-week high price of the financial instrument.
        week_52_low (float): The 52-week low price of the financial instrument.
        bidsize (int): The bid size of the financial instrument (in hundreds).
        bidexch (str): The exchange where the bid price is quoted.
        bid_date (str): The date of the bid price.
        asksize (int): The ask size of the financial instrument.
        askexch (str): The exchange where the ask price is quoted.
        ask_date (str): The date of the ask price.
        open_interest (int, optional): The open interest for options.
        contract_size (str, optional): The contract size for options.
        expiration_date (str, optional): The expiration date for options.
        expiration_type (str, optional): The expiration type for options.
        option_type (OptionType, optional): The type of the option.
        root_symbols (str): Comma-delimited list of option root symbols for an underlier.
        root_symbol (str, optional): The root symbol for an underlier.
        greeks (Greeks, optional): The Greeks values for options.
        note (str, optional): The note for the quote.
    """

    def __init__(self, **kwargs):
        self.symbol = kwargs.get("symbol")
        self.description = kwargs.get("description")
        self.exch = kwargs.get("exch")
        self.type = QuoteType(kwargs.get("type")) if kwargs.get("type") else None
        self.last = kwargs.get("last")
        self.change = kwargs.get("change")
        self.volume = kwargs.get("volume")
        self.open = kwargs.get("open")
        self.high = kwargs.get("high")
        self.low = kwargs.get("low")
        self.close = kwargs.get("close")
        self.bid = kwargs.get("bid")
        self.ask = kwargs.get("ask")
        self.underlying = kwargs.get("underlying", None)
        self.strike = kwargs.get("strike", None)
        self.change_percentage = kwargs.get("change_percentage")
        self.average_volume = kwargs.get("average_volume")  # 90 day average volume
        self.last_volume = kwargs.get("last_volume")  # volume of last price
        self.trade_date = kwargs.get("trade_date")  # most recent trade date
        self.prevclose = kwargs.get("prevclose")
        self.week_52_high = kwargs.get("week_52_high")
        self.week_52_low = kwargs.get("week_52_low")
        self.bidsize = kwargs.get("bidsize")  # in hundreds
        self.bidexch = kwargs.get("bidexch")
        self.bid_date = kwargs.get("bid_date")
        self.asksize = kwargs.get("asksize")
        self.askexch = kwargs.get("askexch")
        self.ask_date = kwargs.get("ask_date")
        self.open_interest = kwargs.get(
            "open_interest", None
        )  # open interest for options
        self.contract_size = kwargs.get("contract_size", None)
        self.expiration_date = kwargs.get("expiration_date", None)
        self.expiration_type = kwargs.get("expiration_type", None)
        self.option_type = (
            OptionType(kwargs.get("option_type"))
            if kwargs.get("option_type", None)
            else None
        )
        self.root_symbols = kwargs.get(
            "root_symbols"
        )  # Comma-delimited list of option root symbols for an underlier
        self.root_symbol = kwargs.get(
            "root_symbol", None
        )  # Root symbol for an underlier

        self.greeks = Greeks(**kwargs.get("greeks")) if kwargs.get("greeks") else None
        self.note = kwargs.get("note", None)
