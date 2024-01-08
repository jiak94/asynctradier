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
    buy = "buy"
    sell = "sell"
    buy_to_cover = "buy_to_cover"
    sell_short = "sell_short"


class OptionOrderSide(StrEnum):
    buy_to_open = "buy_to_open"
    buy_to_close = "buy_to_close"
    sell_to_open = "sell_to_open"
    sell_to_close = "sell_to_close"


class OrderType(StrEnum):
    market = "market"
    limit = "limit"
    stop = "stop"
    stop_limit = "stop_limit"


class Duration(StrEnum):
    day = "day"
    good_till_cancel = "gtc"
    pre = "pre"
    immediate_or_cancel = "post"
