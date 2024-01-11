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


class EquatityOrderSide(StrEnum):
    """
    Represents the order side for equity orders.

    Possible values:
    - buy: for buying equity
    - sell: for selling equity
    - buy_to_cover: for buying to cover a short position
    - sell_short: for selling short
    """

    buy = "buy"
    sell = "sell"
    buy_to_cover = "buy_to_cover"
    sell_short = "sell_short"


class OptionOrderSide(StrEnum):
    """
    Represents the order side for option orders.

    Possible values:
    - buy_to_open: for buying to open an option position
    - buy_to_close: for buying to close an option position
    - sell_to_open: for selling to open an option position
    - sell_to_close: for selling to close an option position
    """

    buy_to_open = "buy_to_open"
    buy_to_close = "buy_to_close"
    sell_to_open = "sell_to_open"
    sell_to_close = "sell_to_close"


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
