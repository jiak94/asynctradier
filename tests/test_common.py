from asynctradier.common import Duration, OrderClass, OrderSide, OrderStatus, OrderType
from asynctradier.common.order import Order


def test_order_equity():
    order_info = {
        "id": 228175,
        "type": "limit",
        "symbol": "AAPL",
        "side": "buy",
        "quantity": 50.00000000,
        "status": "expired",
        "duration": "pre",
        "price": 22.0,
        "avg_fill_price": 0.00000000,
        "exec_quantity": 0.00000000,
        "last_fill_price": 0.00000000,
        "last_fill_quantity": 0.00000000,
        "remaining_quantity": 0.00000000,
        "create_date": "2018-06-01T12:02:29.682Z",
        "transaction_date": "2018-06-01T12:30:02.385Z",
        "class": "equity",
    }

    order = Order(**order_info)

    assert order.id == 228175
    assert order.type == OrderType.limit
    assert order.symbol == "AAPL"
    assert order.side == OrderSide.buy
    assert order.quantity == 50.00000000
    assert order.status == OrderStatus.expired
    assert order.duration == Duration.pre
    assert order.price == 22.0
    assert order.avg_fill_price == 0.00000000
    assert order.exec_quantity == 0.00000000
    assert order.last_fill_price == 0.00000000
    assert order.last_fill_quantity == 0.00000000
    assert order.remaining_quantity == 0.00000000
    assert order.create_date == "2018-06-01T12:02:29.682Z"
    assert order.transaction_date == "2018-06-01T12:30:02.385Z"
    assert order.class_ == OrderClass.equity


def test_order_option():
    order_info = {
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
        "option_symbol": "SPY180720C00274000",
    }

    order = Order(**order_info)

    assert order.id == 228749
    assert order.type == OrderType.market
    assert order.symbol == "SPY"
    assert order.side == OrderSide.buy_to_open
    assert order.quantity == 1.00000000
    assert order.status == OrderStatus.expired
    assert order.duration == Duration.pre
    assert order.avg_fill_price == 0.00000000
    assert order.exec_quantity == 0.00000000
    assert order.last_fill_price == 0.00000000
    assert order.last_fill_quantity == 0.00000000
    assert order.remaining_quantity == 0.00000000
    assert order.create_date == "2018-06-06T20:16:17.342Z"
    assert order.transaction_date == "2018-06-06T20:16:17.357Z"
    assert order.class_ == OrderClass.option
    assert order.option_symbol == "SPY180720C00274000"


def test_order_combo():
    order_info = {
        "id": 229063,
        "type": "debit",
        "symbol": "SPY",
        "side": "buy",
        "quantity": 1.00000000,
        "status": "canceled",
        "duration": "pre",
        "price": 42.0,
        "avg_fill_price": 0.00,
        "exec_quantity": 0.00000000,
        "last_fill_price": 0.00000000,
        "last_fill_quantity": 0.00000000,
        "remaining_quantity": 0.00000000,
        "create_date": "2018-06-12T21:13:36.076Z",
        "transaction_date": "2018-06-12T21:18:41.604Z",
        "class": "combo",
        "num_legs": 2,
        "strategy": "covered call",
        "leg": [
            {
                "id": 229064,
                "type": "debit",
                "symbol": "SPY",
                "side": "buy",
                "quantity": 100.00000000,
                "status": "canceled",
                "duration": "pre",
                "price": 42.0,
                "avg_fill_price": 0.00000000,
                "exec_quantity": 0.00000000,
                "last_fill_price": 0.00000000,
                "last_fill_quantity": 0.00000000,
                "remaining_quantity": 0.00000000,
                "create_date": "2018-06-12T21:13:36.076Z",
                "transaction_date": "2018-06-12T21:18:41.587Z",
                "class": "equity",
            },
            {
                "id": 229065,
                "type": "debit",
                "symbol": "SPY",
                "side": "sell_to_close",
                "quantity": 1.00000000,
                "status": "canceled",
                "duration": "pre",
                "price": 42.0,
                "avg_fill_price": 0.00000000,
                "exec_quantity": 0.00000000,
                "last_fill_price": 0.00000000,
                "last_fill_quantity": 0.00000000,
                "remaining_quantity": 0.00000000,
                "create_date": "2018-06-12T21:13:36.076Z",
                "transaction_date": "2018-06-12T21:18:41.597Z",
                "class": "option",
                "option_symbol": "SPY180720C00274000",
            },
        ],
    }

    order = Order(**order_info)

    assert order.id == 229063
    assert order.type == OrderType.debit
    assert order.symbol == "SPY"
    assert order.side == OrderSide.buy
    assert order.quantity == 1.00000000
    assert order.status == OrderStatus.canceled
    assert order.duration == Duration.pre
    assert order.price == 42.0
    assert order.avg_fill_price == 0.00
    assert order.exec_quantity == 0.00000000
    assert order.last_fill_price == 0.00000000
    assert order.last_fill_quantity == 0.00000000
    assert order.remaining_quantity == 0.00000000
    assert order.create_date == "2018-06-12T21:13:36.076Z"
    assert order.transaction_date == "2018-06-12T21:18:41.604Z"
    assert order.class_ == OrderClass.combo
    assert order.number_of_legs == 2

    for order_leg, leg in zip(order.legs, order_info["leg"]):
        assert order_leg.id == leg["id"]
        assert order_leg.type == OrderType(leg["type"])
        assert order_leg.symbol == "SPY"
        assert order_leg.side == OrderSide(leg["side"])
        assert order_leg.quantity == leg["quantity"]
        assert order_leg.status == OrderStatus(leg["status"])
        assert order_leg.duration == Duration(leg["duration"])
        assert order_leg.price == leg["price"]
        assert order_leg.avg_fill_price == leg["avg_fill_price"]
        assert order_leg.exec_quantity == leg["exec_quantity"]
        assert order_leg.last_fill_price == leg["last_fill_price"]
        assert order_leg.last_fill_quantity == leg["last_fill_quantity"]
        assert order_leg.remaining_quantity == leg["remaining_quantity"]
        assert order_leg.create_date == leg["create_date"]
        assert order_leg.transaction_date == leg["transaction_date"]
        assert order_leg.class_ == OrderClass(leg["class"])


def test_order_multileg():
    order_info = {
        "id": 229123,
        "type": "credit",
        "symbol": "SPY",
        "side": "buy",
        "quantity": 1.00000000,
        "status": "expired",
        "duration": "pre",
        "price": 0.8,
        "avg_fill_price": 0.00,
        "exec_quantity": 0.00000000,
        "last_fill_price": 0.00000000,
        "last_fill_quantity": 0.00000000,
        "remaining_quantity": 0.00000000,
        "create_date": "2018-06-13T16:54:39.812Z",
        "transaction_date": "2018-06-13T20:55:00.069Z",
        "class": "multileg",
        "num_legs": 4,
        "strategy": "condor",
        "leg": [
            {
                "id": 229124,
                "type": "credit",
                "symbol": "SPY",
                "side": "buy_to_open",
                "quantity": 1.00000000,
                "status": "expired",
                "duration": "pre",
                "price": 0.8,
                "avg_fill_price": 0.00000000,
                "exec_quantity": 0.00000000,
                "last_fill_price": 0.00000000,
                "last_fill_quantity": 0.00000000,
                "remaining_quantity": 0.00000000,
                "create_date": "2018-06-13T16:54:39.812Z",
                "transaction_date": "2018-06-13T20:55:00.069Z",
                "class": "option",
                "option_symbol": "SPY180720C00274000",
            },
            {
                "id": 229125,
                "type": "credit",
                "symbol": "SPY",
                "side": "sell_to_open",
                "quantity": 1.00000000,
                "status": "expired",
                "duration": "pre",
                "price": 0.8,
                "avg_fill_price": 0.00000000,
                "exec_quantity": 0.00000000,
                "last_fill_price": 0.00000000,
                "last_fill_quantity": 0.00000000,
                "remaining_quantity": 0.00000000,
                "create_date": "2018-06-13T16:54:39.812Z",
                "transaction_date": "2018-06-13T20:55:00.069Z",
                "class": "option",
                "option_symbol": "SPY180720C00275000",
            },
            {
                "id": 229126,
                "type": "credit",
                "symbol": "SPY",
                "side": "sell_to_open",
                "quantity": 1.00000000,
                "status": "expired",
                "duration": "pre",
                "price": 0.8,
                "avg_fill_price": 0.00000000,
                "exec_quantity": 0.00000000,
                "last_fill_price": 0.00000000,
                "last_fill_quantity": 0.00000000,
                "remaining_quantity": 0.00000000,
                "create_date": "2018-06-13T16:54:39.812Z",
                "transaction_date": "2018-06-13T20:55:00.069Z",
                "class": "option",
                "option_symbol": "SPY180720C00276000",
            },
            {
                "id": 229127,
                "type": "credit",
                "symbol": "SPY",
                "side": "buy_to_open",
                "quantity": 1.00000000,
                "status": "expired",
                "duration": "pre",
                "price": 0.8,
                "avg_fill_price": 0.00000000,
                "exec_quantity": 0.00000000,
                "last_fill_price": 0.00000000,
                "last_fill_quantity": 0.00000000,
                "remaining_quantity": 0.00000000,
                "create_date": "2018-06-13T16:54:39.812Z",
                "transaction_date": "2018-06-13T20:55:00.069Z",
                "class": "option",
                "option_symbol": "SPY180720C00277000",
            },
        ],
    }

    order = Order(**order_info)

    assert order.id == 229123
    assert order.type == OrderType.credit
    assert order.symbol == "SPY"
    assert order.side == OrderSide.buy
    assert order.quantity == 1.00000000
    assert order.status == OrderStatus.expired
    assert order.duration == Duration.pre
    assert order.price == 0.8
    assert order.avg_fill_price == 0.00
    assert order.exec_quantity == 0.00000000
    assert order.last_fill_price == 0.00000000
    assert order.last_fill_quantity == 0.00000000
    assert order.remaining_quantity == 0.00000000
    assert order.create_date == "2018-06-13T16:54:39.812Z"
    assert order.transaction_date == "2018-06-13T20:55:00.069Z"
    assert order.class_ == OrderClass.multileg
    assert order.number_of_legs == 4

    for order_leg, leg in zip(order.legs, order_info["leg"]):
        assert order_leg.id == leg["id"]
        assert order_leg.type == OrderType(leg["type"])
        assert order_leg.symbol == "SPY"
        assert order_leg.side == OrderSide(leg["side"])
        assert order_leg.quantity == leg["quantity"]
        assert order_leg.status == OrderStatus(leg["status"])
        assert order_leg.duration == Duration(leg["duration"])
        assert order_leg.price == leg["price"]
        assert order_leg.avg_fill_price == leg["avg_fill_price"]
        assert order_leg.exec_quantity == leg["exec_quantity"]
        assert order_leg.last_fill_price == leg["last_fill_price"]
        assert order_leg.last_fill_quantity == leg["last_fill_quantity"]
        assert order_leg.remaining_quantity == leg["remaining_quantity"]
        assert order_leg.create_date == leg["create_date"]
        assert order_leg.transaction_date == leg["transaction_date"]
        assert order_leg.class_ == OrderClass(leg["class"])
        assert order_leg.option_symbol == leg["option_symbol"]
