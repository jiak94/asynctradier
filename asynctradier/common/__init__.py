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
