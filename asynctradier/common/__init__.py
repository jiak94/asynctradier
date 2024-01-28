from strenum import StrEnum


class OrderClass(StrEnum):
    """
    Represents the order class for trading.

    Possible values:
    - equity: for equity orders
    - option: for option orders
    - multileg: for multileg orders
    - combo: for combo orders
    """

    equity = "equity"
    option = "option"
    multileg = "multileg"
    combo = "combo"


class OrderSide(StrEnum):
    """
    Enum class representing the different order sides.

    Possible values:
    - buy_to_open: for buying to open
    - buy_to_close: for buying to close
    - sell_to_open: for selling to open
    - sell_to_close: for selling to close
    - buy: for buying
    - sell: for selling
    - buy_to_cover: for buying to cover
    - sell_short: for selling short
    """

    # For option class
    buy_to_open = "buy_to_open"
    buy_to_close = "buy_to_close"
    sell_to_open = "sell_to_open"
    sell_to_close = "sell_to_close"

    # For equity class
    buy = "buy"
    sell = "sell"
    buy_to_cover = "buy_to_cover"
    sell_short = "sell_short"


class OrderType(StrEnum):
    """
    Represents the order type.

    Possible values:
    - market: for market orders
    - limit: for limit orders
    - stop: for stop orders
    - stop_limit: for stop limit orders
    - debit: for debit spread orders
    - credit: for credit spread orders
    - even: for even spread orders
    """

    market = "market"
    limit = "limit"
    stop = "stop"
    stop_limit = "stop_limit"
    debit = "debit"
    credit = "credit"
    even = "even"


class Duration(StrEnum):
    """
    Represents the order duration.

    Possible values:
    - day: for day orders
    - good_till_cancel: for good till cancel orders
    - pre: for pre-market orders
    - immediate_or_cancel: for immediate or cancel orders
    """

    day = "day"
    good_till_cancel = "gtc"
    pre = "pre"
    immediate_or_cancel = "post"


class OrderStatus(StrEnum):
    """
    Represents the status of an order.

    Possible values:
    - open: The order is open and active.
    - partially_filled: The order has been partially filled.
    - filled: The order has been completely filled.
    - expired: The order has expired.
    - canceled: The order has been canceled.
    - rejected: The order has been rejected.
    - pending: The order is pending.
    - error: An error occurred with the order.
    - ok: The order is submitted.
    """

    open = "open"
    partially_filled = "partially_filled"
    filled = "filled"
    expired = "expired"
    canceled = "canceled"
    rejected = "rejected"
    pending = "pending"
    error = "error"
    ok = "ok"


class QuoteType(StrEnum):
    """
    Represents the type of quote.

    Possible values:
    - stock: for stock quotes
    - option: for option quotes
    - index: for index quotes
    - mutual_fund: for mutual fund quotes
    """

    stock = "stock"
    option = "option"
    etf = "etf"
    index = "index"
    mutual_fund = "mutual_fund"


class OptionType(StrEnum):
    """
    Represents the type of option.

    Possible values:
    - call: for call options
    - put: for put options
    """

    call = "call"
    put = "put"


class Classification(StrEnum):
    """
    Enum class representing different classifications.

    Possible values:
    - individual
    - entity
    - joint_survivor
    - traditional_ira
    - roth_ira
    - rollover_ira
    - sep_ira
    """

    individual = "individual"
    entity = "entity"
    joint_survivor = "joint_survivor"
    traditional_ira = "traditional_ira"
    roth_ira = "roth_ira"
    rollover_ira = "rollover_ira"
    sep_ira = "sep_ira"


class AccountStatus(StrEnum):
    """
    Represents the status of an account.

    Attributes:
        open (str): The account is open.
        closed (str): The account is closed.
    """

    active = "active"
    closed = "closed"


class AccountType(StrEnum):
    """
    Represents the type of account.

    Attributes:
        cash (str): The account is a cash account.
        margin (str): The account is a margin account.
        pdt (str): The account is a pattern day trader account.
    """

    cash = "cash"
    margin = "margin"
    pdt = "pdt"


class EventType(StrEnum):
    """
    Represents the type of an event.

    Attributes:
        trade (str): The event is a trade event.
        journal (str): The event is a journal event.
        option (str): The event is an option event.
        ach (str): The event is an ACH event.
        wire (str): The event is a wire event.
        dividend (str): The event is a dividend event.
        fee (str): The event is a fee event.
        tax (str): The event is a tax event.
        check (str): The event is a check event.
        transfer (str): The event is a transfer event.
        adjustment (str): The event is an adjustment event.
        interest (str): The event is an interest event.
    """

    trade = "trade"
    journal = "journal"
    option = "option"
    ach = "ach"
    wire = "wire"
    dividend = "dividend"
    fee = "fee"
    tax = "tax"
    check = "check"
    transfer = "transfer"
    adjustment = "adjustment"
    interest = "interest"


class TradeType(StrEnum):
    """
    Represents the type of a trade.

    Attributes:
        buy (str): The trade is a buy trade.
        sell (str): The trade is a sell trade.
    """

    equity = "equity"
    option = "option"


class MarketStatus(StrEnum):
    """
    Represents the status of the market.

    Attributes:
        open (str): The market is open.
        closed (str): The market is closed.
    """

    open = "open"
    closed = "closed"
