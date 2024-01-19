from asynctradier.common import (
    AccountStatus,
    AccountType,
    Classification,
    Duration,
    OptionType,
    OrderClass,
    OrderSide,
    OrderStatus,
    OrderType,
    QuoteType,
)
from asynctradier.common.account_balance import (
    AccountBalance,
    CashAccountBalanceDetails,
    MarginAccountBalanceDetails,
    PDTAccountBalanceDetails,
)
from asynctradier.common.expiration import Expiration
from asynctradier.common.option_contract import OptionContract
from asynctradier.common.order import Order
from asynctradier.common.quote import Quote
from asynctradier.common.user_profile import UserAccount
from asynctradier.exceptions import InvalidExiprationDate, InvalidOptionType


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


def test_option_contract():
    contract = OptionContract(
        "SPY",
        "2019-03-29",
        274.00,
        OptionType.call,
        OrderSide.buy_to_open,
        1,
    )

    assert contract.symbol == "SPY"
    assert contract.expiration_date == "2019-03-29"
    assert contract.strike == 274.00
    assert contract.option_type == OptionType.call
    assert contract.order_side == OrderSide.buy_to_open
    assert contract.quantity == 1
    assert contract.option_symbol == "SPY190329C00274000"


def test_option_contract_invalid_exp_date():
    try:
        OptionContract(
            "SPY",
            "2019/03/29",
            274.00,
            OptionType.call,
            OrderSide.buy_to_open,
            1,
        )
    except InvalidExiprationDate:
        assert True


def test_option_contract_invalid_option_type():
    try:
        OptionContract(
            "SPY",
            "2019-03-29",
            274.00,
            "invalid",
            OrderSide.buy_to_open,
            1,
        )
    except InvalidOptionType:
        assert True


def test_quote_stock():
    quote_info = {
        "symbol": "AAPL",
        "description": "Apple Inc",
        "exch": "Q",
        "type": "stock",
        "last": 185.815,
        "change": 0.23,
        "volume": 11815107,
        "open": 186.06,
        "high": 186.74,
        "low": 185.19,
        "close": None,
        "bid": 185.81,
        "ask": 185.82,
        "change_percentage": 0.13,
        "average_volume": 54243871,
        "last_volume": 100,
        "trade_date": 1705075974129,
        "prevclose": 185.59,
        "week_52_high": 199.62,
        "week_52_low": 131.66,
        "bidsize": 5,
        "bidexch": "K",
        "bid_date": 1705075974000,
        "asksize": 2,
        "askexch": "Q",
        "ask_date": 1705075974000,
        "root_symbols": "AAPL",
    }

    quote = Quote(**quote_info)

    assert quote.symbol == "AAPL"
    assert quote.description == "Apple Inc"
    assert quote.exch == "Q"
    assert quote.type == QuoteType.stock
    assert quote.last == 185.815
    assert quote.change == 0.23
    assert quote.volume == 11815107
    assert quote.open == 186.06
    assert quote.high == 186.74
    assert quote.low == 185.19
    assert quote.close is None
    assert quote.bid == 185.81
    assert quote.ask == 185.82
    assert quote.change_percentage == 0.13
    assert quote.average_volume == 54243871
    assert quote.last_volume == 100
    assert quote.trade_date == 1705075974129
    assert quote.prevclose == 185.59
    assert quote.week_52_high == 199.62
    assert quote.week_52_low == 131.66
    assert quote.bidsize == 5
    assert quote.bidexch == "K"
    assert quote.bid_date == 1705075974000
    assert quote.asksize == 2
    assert quote.askexch == "Q"
    assert quote.ask_date == 1705075974000
    assert quote.root_symbols == "AAPL"


def test_quote_option():
    quote_info = {
        "symbol": "TSLA240119P00250000",
        "description": "TSLA Jan 19 2024 $250.00 Put",
        "exch": "Z",
        "type": "option",
        "last": 28.64,
        "change": 5.62,
        "volume": 325,
        "open": 28.2,
        "high": 30.28,
        "low": 25.0,
        "close": None,
        "bid": 28.35,
        "ask": 28.75,
        "underlying": "TSLA",
        "strike": 250.0,
        "greeks": {
            "delta": -0.9604526529331165,
            "gamma": 0.005467830085355449,
            "theta": -0.08873705325377128,
            "vega": 0.024449975355968073,
            "rho": 0.0016218090363680116,
            "phi": -0.001667023522931263,
            "bid_iv": 0.0,
            "mid_iv": 0.568797,
            "ask_iv": 0.568797,
            "smv_vol": 0.471,
            "updated_at": "2024-01-12 15:59:03",
        },
        "change_percentage": 24.42,
        "average_volume": 0,
        "last_volume": 20,
        "trade_date": 1705076054411,
        "prevclose": 23.02,
        "week_52_high": 0.0,
        "week_52_low": 0.0,
        "bidsize": 28,
        "bidexch": "P",
        "bid_date": 1705075972000,
        "asksize": 12,
        "askexch": "Z",
        "ask_date": 1705075972000,
        "open_interest": 31812,
        "contract_size": 100,
        "expiration_date": "2024-01-19",
        "expiration_type": "standard",
        "option_type": "put",
        "root_symbol": "TSLA",
    }

    quote = Quote(**quote_info)

    assert quote.symbol == "TSLA240119P00250000"
    assert quote.description == "TSLA Jan 19 2024 $250.00 Put"
    assert quote.exch == "Z"
    assert quote.type == QuoteType.option
    assert quote.last == 28.64
    assert quote.change == 5.62
    assert quote.volume == 325
    assert quote.open == 28.2
    assert quote.high == 30.28
    assert quote.low == 25.0
    assert quote.close is None
    assert quote.bid == 28.35
    assert quote.ask == 28.75
    assert quote.underlying == "TSLA"
    assert quote.strike == 250.0
    assert quote.greeks.delta == -0.9604526529331165
    assert quote.greeks.gamma == 0.005467830085355449
    assert quote.greeks.theta == -0.08873705325377128
    assert quote.greeks.vega == 0.024449975355968073
    assert quote.greeks.rho == 0.0016218090363680116
    assert quote.greeks.phi == -0.001667023522931263
    assert quote.greeks.bid_iv == 0.0
    assert quote.greeks.mid_iv == 0.568797
    assert quote.greeks.ask_iv == 0.568797
    assert quote.greeks.smv_vol == 0.471
    assert quote.greeks.updated_at == "2024-01-12 15:59:03"
    assert quote.change_percentage == 24.42
    assert quote.average_volume == 0
    assert quote.last_volume == 20
    assert quote.trade_date == 1705076054411
    assert quote.prevclose == 23.02
    assert quote.week_52_high == 0.0
    assert quote.week_52_low == 0.0
    assert quote.bidsize == 28
    assert quote.bidexch == "P"
    assert quote.bid_date == 1705075972000
    assert quote.asksize == 12
    assert quote.askexch == "Z"
    assert quote.ask_date == 1705075972000
    assert quote.open_interest == 31812
    assert quote.contract_size == 100
    assert quote.expiration_date == "2024-01-19"
    assert quote.expiration_type == "standard"
    assert quote.option_type == OptionType.put
    assert quote.root_symbol == "TSLA"


def test_expirations():
    expiration_info = {
        "date": "2023-11-10",
        "contract_size": 100,
        "expiration_type": "weeklys",
        "strikes": [
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            18.5,
            19.0,
            19.5,
            20.0,
            20.5,
            21.0,
            21.5,
            22.0,
        ],
    }

    expirations = Expiration(**expiration_info)

    assert expirations.date == "2023-11-10"
    assert expirations.contract_size == 100
    assert expirations.expiration_type == "weeklys"
    print(expirations.strikes)
    assert len(expirations.strikes) == len(expiration_info["strikes"])


def test_userprofile():
    userprofile_info = {
        "id": "id-gcostanza",
        "name": "George Costanza",
        "account_number": "VA000001",
        "classification": "individual",
        "date_created": "2016-08-01T21:08:55.000Z",
        "day_trader": False,
        "option_level": 6,
        "status": "active",
        "type": "margin",
        "last_update_date": "2016-08-01T21:08:55.000Z",
    }

    account = UserAccount(**userprofile_info)

    assert account.id == userprofile_info["id"]
    assert account.name == userprofile_info["name"]
    assert account.account_number == userprofile_info["account_number"]
    assert account.classification == Classification.individual
    assert account.date_created == userprofile_info["date_created"]
    assert account.day_trader is False
    assert account.option_level == 6
    assert account.status == AccountStatus.active
    assert account.type == AccountType.margin
    assert account.last_update_date == userprofile_info["last_update_date"]


def test_cashbalancedetail():
    detail_info = {
        "cash_available": 4343.38000000,
        "sweep": 0,
        "unsettled_funds": 1310.00000000,
    }

    detail = CashAccountBalanceDetails(**detail_info)

    assert detail.cash_available == 4343.38000000
    assert detail.sweep == 0
    assert detail.unsettled_funds == 1310.00000000


def test_marginbalancedetail():
    detail = {
        "fed_call": 0,
        "maintenance_call": 0,
        "option_buying_power": 6363.860000000000000000000000,
        "stock_buying_power": 12727.7200000000000000,
        "stock_short_value": 0,
        "sweep": 0,
    }

    detail = MarginAccountBalanceDetails(**detail)

    assert detail.fed_call == 0
    assert detail.maintenance_call == 0
    assert detail.option_buying_power == 6363.860000000000000000000000
    assert detail.stock_buying_power == 12727.7200000000000000
    assert detail.stock_short_value == 0
    assert detail.sweep == 0


def test_pdfbalancedetail():
    detail = {
        "fed_call": 0,
        "maintenance_call": 0,
        "option_buying_power": 6363.860000000000000000000000,
        "stock_buying_power": 12727.7200000000000000,
        "stock_short_value": 0,
    }

    detail = PDTAccountBalanceDetails(**detail)

    assert detail.fed_call == 0
    assert detail.maintenance_call == 0
    assert detail.option_buying_power == 6363.860000000000000000000000
    assert detail.stock_buying_power == 12727.7200000000000000
    assert detail.stock_short_value == 0


def test_balance_margin():
    detail = {
        "option_short_value": 0,
        "total_equity": 17798.360000000000000000000000,
        "account_number": "VA00000000",
        "account_type": "margin",
        "close_pl": -4813.000000000000000000,
        "current_requirement": 2557.00000000000000000000,
        "equity": 0,
        "long_market_value": 11434.50000000000000000000,
        "market_value": 11434.50000000000000000000,
        "open_pl": 546.900000000000000000000000,
        "option_long_value": 8877.5000000000000000000,
        "option_requirement": 0,
        "pending_orders_count": 0,
        "short_market_value": 0,
        "stock_long_value": 2557.00000000000000000000,
        "total_cash": 6363.860000000000000000000000,
        "uncleared_funds": 0,
        "pending_cash": 0,
        "margin": {
            "fed_call": 0,
            "maintenance_call": 0,
            "option_buying_power": 6363.860000000000000000000000,
            "stock_buying_power": 12727.7200000000000000,
            "stock_short_value": 0,
            "sweep": 0,
        },
    }

    balance = AccountBalance(**detail)

    assert balance.option_short_value == detail["option_short_value"]
    assert balance.total_equity == detail["total_equity"]
    assert balance.account_number == detail["account_number"]
    assert balance.account_type == AccountType.margin
    assert balance.close_pl == detail["close_pl"]
    assert balance.current_requirement == detail["current_requirement"]
    assert balance.equity == detail["equity"]
    assert balance.long_market_value == detail["long_market_value"]
    assert balance.market_value == detail["market_value"]
    assert balance.open_pl == detail["open_pl"]
    assert balance.option_long_value == detail["option_long_value"]
    assert balance.option_requirement == detail["option_requirement"]
    assert balance.pending_orders_count == detail["pending_orders_count"]
    assert balance.short_market_value == detail["short_market_value"]
    assert balance.stock_long_value == detail["stock_long_value"]
    assert balance.total_cash == detail["total_cash"]
    assert balance.uncleared_funds == detail["uncleared_funds"]
    assert balance.pending_cash == detail["pending_cash"]

    assert balance.margin.fed_call == detail["margin"]["fed_call"]
    assert balance.margin.maintenance_call == detail["margin"]["maintenance_call"]
    assert balance.margin.option_buying_power == detail["margin"]["option_buying_power"]
    assert balance.margin.stock_buying_power == detail["margin"]["stock_buying_power"]
    assert balance.margin.stock_short_value == detail["margin"]["stock_short_value"]
    assert balance.margin.sweep == detail["margin"]["sweep"]

    assert balance.cash is None
    assert balance.pdt is None


def test_balance_cash():
    detail = {
        "option_short_value": 0,
        "total_equity": 17798.360000000000000000000000,
        "account_number": "VA00000000",
        "account_type": "margin",
        "close_pl": -4813.000000000000000000,
        "current_requirement": 2557.00000000000000000000,
        "equity": 0,
        "long_market_value": 11434.50000000000000000000,
        "market_value": 11434.50000000000000000000,
        "open_pl": 546.900000000000000000000000,
        "option_long_value": 8877.5000000000000000000,
        "option_requirement": 0,
        "pending_orders_count": 0,
        "short_market_value": 0,
        "stock_long_value": 2557.00000000000000000000,
        "total_cash": 6363.860000000000000000000000,
        "uncleared_funds": 0,
        "pending_cash": 0,
        "cash": {
            "cash_available": 4343.38000000,
            "sweep": 0,
            "unsettled_funds": 1310.00000000,
        },
    }

    balance = AccountBalance(**detail)

    assert balance.option_short_value == detail["option_short_value"]
    assert balance.total_equity == detail["total_equity"]
    assert balance.account_number == detail["account_number"]
    assert balance.account_type == AccountType.margin
    assert balance.close_pl == detail["close_pl"]
    assert balance.current_requirement == detail["current_requirement"]
    assert balance.equity == detail["equity"]
    assert balance.long_market_value == detail["long_market_value"]
    assert balance.market_value == detail["market_value"]
    assert balance.open_pl == detail["open_pl"]
    assert balance.option_long_value == detail["option_long_value"]
    assert balance.option_requirement == detail["option_requirement"]
    assert balance.pending_orders_count == detail["pending_orders_count"]
    assert balance.short_market_value == detail["short_market_value"]
    assert balance.stock_long_value == detail["stock_long_value"]
    assert balance.total_cash == detail["total_cash"]
    assert balance.uncleared_funds == detail["uncleared_funds"]
    assert balance.pending_cash == detail["pending_cash"]

    assert balance.cash.cash_available == detail["cash"]["cash_available"]
    assert balance.cash.sweep == detail["cash"]["sweep"]
    assert balance.cash.unsettled_funds == detail["cash"]["unsettled_funds"]

    assert balance.margin is None
    assert balance.pdt is None


def test_balance_pdt():
    detail = {
        "option_short_value": 0,
        "total_equity": 17798.360000000000000000000000,
        "account_number": "VA00000000",
        "account_type": "margin",
        "close_pl": -4813.000000000000000000,
        "current_requirement": 2557.00000000000000000000,
        "equity": 0,
        "long_market_value": 11434.50000000000000000000,
        "market_value": 11434.50000000000000000000,
        "open_pl": 546.900000000000000000000000,
        "option_long_value": 8877.5000000000000000000,
        "option_requirement": 0,
        "pending_orders_count": 0,
        "short_market_value": 0,
        "stock_long_value": 2557.00000000000000000000,
        "total_cash": 6363.860000000000000000000000,
        "uncleared_funds": 0,
        "pending_cash": 0,
        "pdt": {
            "fed_call": 0,
            "maintenance_call": 0,
            "option_buying_power": 6363.860000000000000000000000,
            "stock_buying_power": 12727.7200000000000000,
            "stock_short_value": 0,
        },
    }
    balance = AccountBalance(**detail)

    assert balance.option_short_value == detail["option_short_value"]
    assert balance.total_equity == detail["total_equity"]
    assert balance.account_number == detail["account_number"]
    assert balance.account_type == AccountType.margin
    assert balance.close_pl == detail["close_pl"]
    assert balance.current_requirement == detail["current_requirement"]
    assert balance.equity == detail["equity"]
    assert balance.long_market_value == detail["long_market_value"]
    assert balance.market_value == detail["market_value"]
    assert balance.open_pl == detail["open_pl"]
    assert balance.option_long_value == detail["option_long_value"]
    assert balance.option_requirement == detail["option_requirement"]
    assert balance.pending_orders_count == detail["pending_orders_count"]
    assert balance.short_market_value == detail["short_market_value"]
    assert balance.stock_long_value == detail["stock_long_value"]
    assert balance.total_cash == detail["total_cash"]
    assert balance.uncleared_funds == detail["uncleared_funds"]
    assert balance.pending_cash == detail["pending_cash"]

    assert balance.pdt.fed_call == detail["pdt"]["fed_call"]
    assert balance.pdt.maintenance_call == detail["pdt"]["maintenance_call"]
    assert balance.pdt.option_buying_power == detail["pdt"]["option_buying_power"]

    assert balance.margin is None
    assert balance.cash is None
