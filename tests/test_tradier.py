from unittest.mock import call

import pytest

from asynctradier.common import (
    AccountType,
    Duration,
    EventType,
    OptionType,
    OrderSide,
    OrderType,
)
from asynctradier.common.option_contract import OptionContract
from asynctradier.exceptions import (
    APINotAvailable,
    InvalidDateFormat,
    InvalidExiprationDate,
    InvalidParameter,
    MissingRequiredParameter,
)
from asynctradier.tradier import TradierClient


def test_tradier_init():
    tradier_client = TradierClient("account_id", "access_token", sandbox=True)
    assert tradier_client.account_id == "account_id"
    assert tradier_client.token == "access_token"
    assert tradier_client.session.base_url == "https://sandbox.tradier.com"

    tradier_client = TradierClient("account_id", "access_token", sandbox=False)
    assert tradier_client.account_id == "account_id"
    assert tradier_client.token == "access_token"
    assert tradier_client.session.base_url == "https://api.tradier.com"


@pytest.mark.asyncio
async def test_get_positions_single(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "positions": {
                "position": {
                    "cost_basis": 207.01,
                    "date_acquired": "2018-08-08T14:41:11.405Z",
                    "id": 130089,
                    "quantity": 1.00000000,
                    "symbol": "AAPL",
                },
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    positions = await tradier_client.get_positions()
    assert len(positions) == 1
    tradier_client.session.get.assert_called_once_with(
        "/v1/accounts/account_id/positions"
    )


@pytest.mark.asyncio
async def test_get_positions_multiple(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "positions": {
                "position": [
                    {
                        "cost_basis": 207.01,
                        "date_acquired": "2018-08-08T14:41:11.405Z",
                        "id": 130089,
                        "quantity": 1.00000000,
                        "symbol": "AAPL",
                    },
                    {
                        "cost_basis": 1870.70,
                        "date_acquired": "2018-08-08T14:42:00.774Z",
                        "id": 130090,
                        "quantity": 1.00000000,
                        "symbol": "AMZN",
                    },
                    {
                        "cost_basis": 50.41,
                        "date_acquired": "2019-01-31T17:05:44.674Z",
                        "id": 133590,
                        "quantity": 1.00000000,
                        "symbol": "CAH",
                    },
                    {
                        "cost_basis": 173.04,
                        "date_acquired": "2019-03-11T16:51:51.987Z",
                        "id": 134134,
                        "quantity": 1.00000000,
                        "symbol": "FB",
                    },
                ]
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    positions = await tradier_client.get_positions()
    assert len(positions) == 4
    tradier_client.session.get.assert_called_once_with(
        "/v1/accounts/account_id/positions"
    )


@pytest.mark.asyncio
async def test_get_order(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "order": {
                "id": 123456,
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
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    order = await tradier_client.get_order("123456")
    assert order.id == 123456
    assert order.type == "market"
    assert order.symbol == "SPY"
    assert order.side == "buy_to_open"
    assert order.quantity == 1.00000000
    assert order.status == "expired"
    assert order.duration == "pre"
    assert order.avg_fill_price == 0.00000000
    assert order.exec_quantity == 0.00000000
    assert order.last_fill_price == 0.00000000
    assert order.last_fill_quantity == 0.00000000
    assert order.remaining_quantity == 0.00000000
    assert order.create_date == "2018-06-06T20:16:17.342Z"
    assert order.transaction_date == "2018-06-06T20:16:17.357Z"
    assert order.class_ == "option"
    assert order.option_symbol == "SPY180720C00274000"

    tradier_client.session.get.assert_called_once_with(
        "/v1/accounts/account_id/orders/123456", params={"includeTags": "true"}
    )


@pytest.mark.asyncio
async def test_buy_option(mocker, tradier_client):
    def mock_post(path: str, params: dict = None, data: dict = None):
        return {
            "order": {
                "id": 257459,
                "status": "ok",
                "partner_id": "c4998eb7-06e8-4820-a7ab-55d9760065fb",
            }
        }

    mocker.patch.object(tradier_client.session, "post", side_effect=mock_post)

    await tradier_client.buy_option(
        "SPY",
        "2019-03-29",
        274.00,
        OptionType.call,
        1,
        OrderType.market,
        Duration.good_till_cancel,
    )
    tradier_client.session.post.assert_called_once_with(
        "/v1/accounts/account_id/orders",
        data={
            "class": "option",
            "symbol": "SPY",
            "option_symbol": "SPY190329C00274000",
            "side": "buy_to_open",
            "quantity": "1",
            "type": "market",
            "duration": "gtc",
            "price": "",
            "stop": "",
            "tag": None,
        },
    )


@pytest.mark.asyncio
async def test_sell_option(mocker, tradier_client):
    def mock_post(path: str, params: dict = None, data: dict = None):
        return {
            "order": {
                "id": 257459,
                "status": "ok",
                "partner_id": "c4998eb7-06e8-4820-a7ab-55d9760065fb",
            }
        }

    mocker.patch.object(tradier_client.session, "post", side_effect=mock_post)

    await tradier_client.sell_option(
        "SPY",
        "2019-03-29",
        274.00,
        OptionType.call,
        1,
        OrderType.market,
        Duration.good_till_cancel,
    )
    tradier_client.session.post.assert_called_once_with(
        "/v1/accounts/account_id/orders",
        data={
            "class": "option",
            "symbol": "SPY",
            "option_symbol": "SPY190329C00274000",
            "side": "sell_to_close",
            "quantity": "1",
            "type": "market",
            "duration": "gtc",
            "price": "",
            "stop": "",
            "tag": None,
        },
    )


@pytest.mark.asyncio
async def test_cancel_order(mocker, tradier_client):
    def mock_delete(path: str, params: dict = None):
        return {"order": {"id": 123456, "status": "ok"}}

    mocker.patch.object(tradier_client.session, "delete", side_effect=mock_delete)

    await tradier_client.cancel_order("123456")
    tradier_client.session.delete.assert_called_once_with(
        "/v1/accounts/account_id/orders/123456"
    )


@pytest.mark.asyncio
async def test_get_orders_single(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        if params.get("page") == 2:
            return {"orders": "null"}
        return {
            "orders": {
                "order": {
                    "id": 123456,
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
                },
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    orders = await tradier_client.get_orders()
    assert len(orders) == 1
    assert orders[0].id == 123456
    assert orders[0].type == "market"
    assert orders[0].symbol == "SPY"
    assert orders[0].side == "buy_to_open"
    assert orders[0].quantity == 1.00000000
    assert orders[0].status == "expired"
    assert orders[0].duration == "pre"
    assert orders[0].avg_fill_price == 0.00000000
    assert orders[0].exec_quantity == 0.00000000
    assert orders[0].last_fill_price == 0.00000000
    assert orders[0].last_fill_quantity == 0.00000000
    assert orders[0].remaining_quantity == 0.00000000
    assert orders[0].create_date == "2018-06-06T20:16:17.342Z"
    assert orders[0].transaction_date == "2018-06-06T20:16:17.357Z"
    assert orders[0].class_ == "option"
    assert orders[0].option_symbol == "SPY180720C00274000"
    tradier_client.session.get.assert_has_calls(
        [
            call(
                "/v1/accounts/account_id/orders",
                params={"page": 1, "includeTags": "true"},
            ),
            call(
                "/v1/accounts/account_id/orders",
                params={"page": 2, "includeTags": "true"},
            ),
        ]
    )


@pytest.mark.asyncio
async def test_get_orders_multiple(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        if params.get("page") == 2:
            return {"orders": "null"}
        return {
            "orders": {
                "order": [
                    {
                        "id": 123456,
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
                    },
                    {
                        "id": 123457,
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
                    },
                ]
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    orders = await tradier_client.get_orders()
    assert len(orders) == 2
    tradier_client.session.get.assert_has_calls(
        [
            call(
                "/v1/accounts/account_id/orders",
                params={"page": 1, "includeTags": "true"},
            ),
            call(
                "/v1/accounts/account_id/orders",
                params={"page": 2, "includeTags": "true"},
            ),
        ]
    )


@pytest.mark.asyncio
async def test_modify_order(mocker, tradier_client):
    def mock_put(path: str, data: dict = None):
        return {
            "order": {
                "id": 123456,
                "status": "ok",
                "partner_id": "c4998eb7-06e8-4820-a7ab-55d9760065fb",
            }
        }

    mocker.patch.object(tradier_client.session, "put", side_effect=mock_put)

    await tradier_client.modify_order("123456", OrderType.market, Duration.day)
    tradier_client.session.put.assert_called_with(
        "/v1/accounts/account_id/orders/123456",
        data={
            "type": "market",
            "duration": "day",
        },
    )
    await tradier_client.modify_order("123456", order_type=OrderType.stop, stop=1.0)
    tradier_client.session.put.assert_called_with(
        "/v1/accounts/account_id/orders/123456",
        data={
            "type": "stop",
            "stop": 1.0,
        },
    )
    await tradier_client.modify_order("123456", order_type=OrderType.limit, price=1.0)
    tradier_client.session.put.assert_called_with(
        "/v1/accounts/account_id/orders/123456",
        data={
            "type": "limit",
            "price": 1.0,
        },
    )


@pytest.mark.asyncio
async def test_multileg(mocker, tradier_client):
    def mock_post(path: str, params: dict = None, data: dict = None):
        return {
            "order": {
                "id": 257459,
                "status": "ok",
                "partner_id": "c4998eb7-06e8-4820-a7ab-55d9760065fb",
            }
        }

    mocker.patch.object(tradier_client.session, "post", side_effect=mock_post)

    contracts = [
        OptionContract(
            "SPY",
            "2019-03-29",
            274.00,
            OptionType.call,
            OrderSide.buy_to_open,
            1,
        ),
        OptionContract(
            "SPY",
            "2019-03-29",
            270.00,
            OptionType.put,
            OrderSide.buy_to_open,
            1,
        ),
    ]

    await tradier_client.multileg(
        symbol="SPY",
        order_type=OrderType.market,
        duration=Duration.good_till_cancel,
        legs=contracts,
    )

    tradier_client.session.post.assert_called_with(
        "/v1/accounts/account_id/orders",
        data={
            "class": "multileg",
            "symbol": "SPY",
            "type": "market",
            "duration": "gtc",
            "option_symbol[0]": "SPY190329C00274000",
            "side[0]": "buy_to_open",
            "quantity[0]": "1",
            "option_symbol[1]": "SPY190329P00270000",
            "side[1]": "buy_to_open",
            "quantity[1]": "1",
        },
    )


@pytest.mark.asyncio
async def test_get_quotes_single(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "quotes": {
                "quote": {
                    "symbol": "AAPL",
                    "description": "Apple Inc",
                    "exch": "Q",
                    "type": "stock",
                    "last": 186.07,
                    "change": 0.48,
                    "volume": 6674105,
                    "open": 186.06,
                    "high": 186.74,
                    "low": 185.485,
                    "close": None,
                    "bid": 186.08,
                    "ask": 186.09,
                    "change_percentage": 0.26,
                    "average_volume": 54243871,
                    "last_volume": 100,
                    "trade_date": 1705072233914,
                    "prevclose": 185.59,
                    "week_52_high": 199.62,
                    "week_52_low": 131.66,
                    "bidsize": 2,
                    "bidexch": "Q",
                    "bid_date": 1705072235000,
                    "asksize": 3,
                    "askexch": "Q",
                    "ask_date": 1705072235000,
                    "root_symbols": "AAPL",
                },
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    quotes = await tradier_client.get_quotes(["AAPL"])
    assert len(quotes) == 1
    assert quotes[0].symbol == "AAPL"
    assert quotes[0].description == "Apple Inc"
    assert quotes[0].exch == "Q"
    assert quotes[0].type == "stock"
    assert quotes[0].last == 186.07
    assert quotes[0].change == 0.48
    assert quotes[0].volume == 6674105
    assert quotes[0].open == 186.06
    assert quotes[0].high == 186.74
    assert quotes[0].low == 185.485
    assert quotes[0].close is None
    assert quotes[0].bid == 186.08
    assert quotes[0].ask == 186.09
    assert quotes[0].change_percentage == 0.26
    assert quotes[0].average_volume == 54243871
    assert quotes[0].last_volume == 100
    assert quotes[0].trade_date == 1705072233914
    assert quotes[0].prevclose == 185.59
    assert quotes[0].week_52_high == 199.62
    assert quotes[0].week_52_low == 131.66
    assert quotes[0].bidsize == 2
    assert quotes[0].bidexch == "Q"
    assert quotes[0].bid_date == 1705072235000
    assert quotes[0].asksize == 3
    assert quotes[0].askexch == "Q"
    assert quotes[0].ask_date == 1705072235000
    assert quotes[0].root_symbols == "AAPL"

    tradier_client.session.get.assert_called_once_with(
        "/v1/markets/quotes", params={"symbols": "AAPL", "greeks": "false"}
    )


@pytest.mark.asyncio
async def test_get_quotes_multiple(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "quotes": {
                "quote": [
                    {
                        "symbol": "AAPL",
                        "description": "Apple Inc",
                        "exch": "Q",
                        "type": "stock",
                        "last": 185.565,
                        "change": -0.03,
                        "volume": 10945550,
                        "open": 186.06,
                        "high": 186.74,
                        "low": 185.19,
                        "close": None,
                        "bid": 185.54,
                        "ask": 185.55,
                        "change_percentage": -0.02,
                        "average_volume": 54243871,
                        "last_volume": 700,
                        "trade_date": 1705075278892,
                        "prevclose": 185.59,
                        "week_52_high": 199.62,
                        "week_52_low": 131.66,
                        "bidsize": 2,
                        "bidexch": "Q",
                        "bid_date": 1705075279000,
                        "asksize": 3,
                        "askexch": "Q",
                        "ask_date": 1705075279000,
                        "root_symbols": "AAPL",
                    },
                    {
                        "symbol": "TSLA240119P00250000",
                        "description": "TSLA Jan 19 2024 $250.00 Put",
                        "exch": "Z",
                        "type": "option",
                        "last": 29.22,
                        "change": 6.20,
                        "volume": 298,
                        "open": 28.2,
                        "high": 30.28,
                        "low": 25.0,
                        "close": None,
                        "bid": 28.9,
                        "ask": 29.3,
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
                        "change_percentage": 26.94,
                        "average_volume": 0,
                        "last_volume": 1,
                        "trade_date": 1705075265186,
                        "prevclose": 23.02,
                        "week_52_high": 0.0,
                        "week_52_low": 0.0,
                        "bidsize": 60,
                        "bidexch": "U",
                        "bid_date": 1705075142000,
                        "asksize": 29,
                        "askexch": "N",
                        "ask_date": 1705075195000,
                        "open_interest": 31812,
                        "contract_size": 100,
                        "expiration_date": "2024-01-19",
                        "expiration_type": "standard",
                        "option_type": "put",
                        "root_symbol": "TSLA",
                    },
                ]
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    quotes = await tradier_client.get_quotes(["AAPL", "TSLA240119P00250000"])

    assert len(quotes) == 2

    tradier_client.session.get.assert_called_once_with(
        "/v1/markets/quotes",
        params={"symbols": "AAPL,TSLA240119P00250000", "greeks": "false"},
    )


@pytest.mark.asyncio
async def test_get_quotes_unmatched_symbol(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {"quotes": {"unmatched_symbols": {"symbol": "SEFDF"}}}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    quotes = await tradier_client.get_quotes(["SEFDF"])
    assert len(quotes) == 1
    assert quotes[0].symbol == "SEFDF"
    assert quotes[0].note == "unmatched symbol"

    tradier_client.session.get.assert_called_once_with(
        "/v1/markets/quotes", params={"symbols": "SEFDF", "greeks": "false"}
    )


@pytest.mark.asyncio
async def test_get_quotes_parts_unmatch_symbol(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "quotes": {
                "quote": {
                    "symbol": "AAPL",
                    "description": "Apple Inc",
                    "exch": "Q",
                    "type": "stock",
                    "last": 185.75,
                    "change": 0.16,
                    "volume": 11189867,
                    "open": 186.06,
                    "high": 186.74,
                    "low": 185.19,
                    "close": None,
                    "bid": 185.74,
                    "ask": 185.75,
                    "change_percentage": 0.09,
                    "average_volume": 54243871,
                    "last_volume": 400,
                    "trade_date": 1705075482942,
                    "prevclose": 185.59,
                    "week_52_high": 199.62,
                    "week_52_low": 131.66,
                    "bidsize": 5,
                    "bidexch": "N",
                    "bid_date": 1705075483000,
                    "asksize": 2,
                    "askexch": "Q",
                    "ask_date": 1705075483000,
                    "root_symbols": "AAPL",
                },
                "unmatched_symbols": {"symbol": "SEFDF"},
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    quotes = await tradier_client.get_quotes(["AAPL", "SEFDF"])
    assert len(quotes) == 2
    assert quotes[0].symbol == "AAPL"
    assert quotes[0].note is None
    assert quotes[1].symbol == "SEFDF"
    assert quotes[1].note == "unmatched symbol"

    tradier_client.session.get.assert_called_once_with(
        "/v1/markets/quotes", params={"symbols": "AAPL,SEFDF", "greeks": "false"}
    )


@pytest.mark.asyncio
async def test_get_quotes_with_greeks(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "quotes": {
                "quote": {
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
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    quotes = await tradier_client.get_quotes(["TSLA240119P00250000"], greeks=True)

    assert len(quotes) == 1
    assert quotes[0].greeks is not None

    tradier_client.session.get.assert_called_once_with(
        "/v1/markets/quotes",
        params={"symbols": "TSLA240119P00250000", "greeks": "true"},
    )


@pytest.mark.asyncio
async def test_get_option_chains(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "options": {
                "option": [
                    {
                        "symbol": "TSLA240119P00290000",
                        "description": "TSLA Jan 19 2024 $290.00 Put",
                        "exch": "Z",
                        "type": "option",
                        "last": 62.16,
                        "change": 0.00,
                        "volume": 0,
                        "open": None,
                        "high": None,
                        "low": None,
                        "close": None,
                        "bid": 70.25,
                        "ask": 74.1,
                        "underlying": "TSLA",
                        "strike": 290.0,
                        "greeks": {
                            "delta": -0.9998557711335186,
                            "gamma": 3.5165824253684816e-5,
                            "theta": -7.229633668219417e-4,
                            "vega": 1.9028779215795382e-4,
                            "rho": 6.64036071274819e-6,
                            "phi": -6.7701434035364e-6,
                            "bid_iv": 0.0,
                            "mid_iv": 1.282883,
                            "ask_iv": 1.282883,
                            "smv_vol": 0.634,
                            "updated_at": "2024-01-12 16:59:08",
                        },
                        "change_percentage": 0.00,
                        "average_volume": 0,
                        "last_volume": 1220,
                        "trade_date": 1705004512652,
                        "prevclose": 62.16,
                        "week_52_high": 0.0,
                        "week_52_low": 0.0,
                        "bidsize": 51,
                        "bidexch": "N",
                        "bid_date": 1705079354000,
                        "asksize": 51,
                        "askexch": "N",
                        "ask_date": 1705079354000,
                        "open_interest": 835,
                        "contract_size": 100,
                        "expiration_date": "2024-01-19",
                        "expiration_type": "standard",
                        "option_type": "put",
                        "root_symbol": "TSLA",
                    },
                    {
                        "symbol": "TSLA240119C00290000",
                        "description": "TSLA Jan 19 2024 $290.00 Call",
                        "exch": "Z",
                        "type": "option",
                        "last": 0.02,
                        "change": -0.02,
                        "volume": 619,
                        "open": 0.03,
                        "high": 0.03,
                        "low": 0.01,
                        "close": None,
                        "bid": 0.01,
                        "ask": 0.02,
                        "underlying": "TSLA",
                        "strike": 290.0,
                        "greeks": {
                            "delta": 1.4422886648140625e-4,
                            "gamma": 3.5165824253684816e-5,
                            "theta": -7.229633668219417e-4,
                            "vega": 1.9028779215795382e-4,
                            "rho": 6.64036071274819e-6,
                            "phi": -6.7701434035364e-6,
                            "bid_iv": 0.679611,
                            "mid_iv": 0.701844,
                            "ask_iv": 0.724077,
                            "smv_vol": 0.634,
                            "updated_at": "2024-01-12 16:59:08",
                        },
                        "change_percentage": -50.00,
                        "average_volume": 0,
                        "last_volume": 4,
                        "trade_date": 1705078886958,
                        "prevclose": 0.04,
                        "week_52_high": 0.0,
                        "week_52_low": 0.0,
                        "bidsize": 1075,
                        "bidexch": "D",
                        "bid_date": 1705079341000,
                        "asksize": 614,
                        "askexch": "D",
                        "ask_date": 1705079341000,
                        "open_interest": 18077,
                        "contract_size": 100,
                        "expiration_date": "2024-01-19",
                        "expiration_type": "standard",
                        "option_type": "call",
                        "root_symbol": "TSLA",
                    },
                ]
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    options = await tradier_client.get_option_chains("TSLA", "2024-01-19")
    assert len(options) == 2

    tradier_client.session.get.assert_called_once_with(
        "/v1/markets/options/chains",
        params={"symbol": "TSLA", "expiration": "2024-01-19", "greeks": "false"},
    )


@pytest.mark.asyncio
async def test_get_option_chains_filter(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "options": {
                "option": [
                    {
                        "symbol": "TSLA240119P00290000",
                        "description": "TSLA Jan 19 2024 $290.00 Put",
                        "exch": "Z",
                        "type": "option",
                        "last": 62.16,
                        "change": 0.00,
                        "volume": 0,
                        "open": None,
                        "high": None,
                        "low": None,
                        "close": None,
                        "bid": 70.25,
                        "ask": 74.1,
                        "underlying": "TSLA",
                        "strike": 290.0,
                        "greeks": {
                            "delta": -0.9998557711335186,
                            "gamma": 3.5165824253684816e-5,
                            "theta": -7.229633668219417e-4,
                            "vega": 1.9028779215795382e-4,
                            "rho": 6.64036071274819e-6,
                            "phi": -6.7701434035364e-6,
                            "bid_iv": 0.0,
                            "mid_iv": 1.282883,
                            "ask_iv": 1.282883,
                            "smv_vol": 0.634,
                            "updated_at": "2024-01-12 16:59:08",
                        },
                        "change_percentage": 0.00,
                        "average_volume": 0,
                        "last_volume": 1220,
                        "trade_date": 1705004512652,
                        "prevclose": 62.16,
                        "week_52_high": 0.0,
                        "week_52_low": 0.0,
                        "bidsize": 51,
                        "bidexch": "N",
                        "bid_date": 1705079354000,
                        "asksize": 51,
                        "askexch": "N",
                        "ask_date": 1705079354000,
                        "open_interest": 835,
                        "contract_size": 100,
                        "expiration_date": "2024-01-19",
                        "expiration_type": "standard",
                        "option_type": "put",
                        "root_symbol": "TSLA",
                    },
                    {
                        "symbol": "TSLA240119C00290000",
                        "description": "TSLA Jan 19 2024 $290.00 Call",
                        "exch": "Z",
                        "type": "option",
                        "last": 0.02,
                        "change": -0.02,
                        "volume": 619,
                        "open": 0.03,
                        "high": 0.03,
                        "low": 0.01,
                        "close": None,
                        "bid": 0.01,
                        "ask": 0.02,
                        "underlying": "TSLA",
                        "strike": 290.0,
                        "greeks": {
                            "delta": 1.4422886648140625e-4,
                            "gamma": 3.5165824253684816e-5,
                            "theta": -7.229633668219417e-4,
                            "vega": 1.9028779215795382e-4,
                            "rho": 6.64036071274819e-6,
                            "phi": -6.7701434035364e-6,
                            "bid_iv": 0.679611,
                            "mid_iv": 0.701844,
                            "ask_iv": 0.724077,
                            "smv_vol": 0.634,
                            "updated_at": "2024-01-12 16:59:08",
                        },
                        "change_percentage": -50.00,
                        "average_volume": 0,
                        "last_volume": 4,
                        "trade_date": 1705078886958,
                        "prevclose": 0.04,
                        "week_52_high": 0.0,
                        "week_52_low": 0.0,
                        "bidsize": 1075,
                        "bidexch": "D",
                        "bid_date": 1705079341000,
                        "asksize": 614,
                        "askexch": "D",
                        "ask_date": 1705079341000,
                        "open_interest": 18077,
                        "contract_size": 100,
                        "expiration_date": "2024-01-19",
                        "expiration_type": "standard",
                        "option_type": "call",
                        "root_symbol": "TSLA",
                    },
                ]
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    options = await tradier_client.get_option_chains(
        "TSLA", "2024-01-19", option_type=OptionType.put
    )

    assert len(options) == 1

    assert options[0].symbol == "TSLA240119P00290000"
    assert options[0].description == "TSLA Jan 19 2024 $290.00 Put"
    assert options[0].exch == "Z"
    assert options[0].type == "option"
    assert options[0].last == 62.16
    assert options[0].change == 0.00
    assert options[0].volume == 0
    assert options[0].open is None
    assert options[0].high is None
    assert options[0].low is None
    assert options[0].close is None
    assert options[0].bid == 70.25
    assert options[0].ask == 74.1
    assert options[0].underlying == "TSLA"
    assert options[0].strike == 290.0
    assert options[0].greeks is not None
    assert options[0].change_percentage == 0.00
    assert options[0].average_volume == 0
    assert options[0].last_volume == 1220
    assert options[0].trade_date == 1705004512652
    assert options[0].prevclose == 62.16
    assert options[0].week_52_high == 0.0
    assert options[0].week_52_low == 0.0
    assert options[0].bidsize == 51
    assert options[0].bidexch == "N"
    assert options[0].bid_date == 1705079354000
    assert options[0].asksize == 51
    assert options[0].askexch == "N"
    assert options[0].ask_date == 1705079354000
    assert options[0].open_interest == 835
    assert options[0].contract_size == 100
    assert options[0].expiration_date == "2024-01-19"
    assert options[0].expiration_type == "standard"
    assert options[0].option_type == "put"
    assert options[0].root_symbol == "TSLA"

    tradier_client.session.get.assert_called_once_with(
        "/v1/markets/options/chains",
        params={"symbol": "TSLA", "expiration": "2024-01-19", "greeks": "false"},
    )


@pytest.mark.asyncio
async def test_get_option_chains_invalid_symbol(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {"options": None}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    options = await tradier_client.get_option_chains("sfefd", "2024-01-19")
    assert len(options) == 0


@pytest.mark.asyncio
async def test_get_option_chains_invalid_date(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {"options": None}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    try:
        await tradier_client.get_option_chains("TSLA", "2024/01/19")
    except InvalidExiprationDate:
        assert True


@pytest.mark.asyncio
async def test_get_option_strikes(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "strikes": {
                "strike": [
                    22.5,
                    25.0,
                    27.5,
                    30.0,
                    32.5,
                    35.0,
                    37.5,
                    40.0,
                    42.5,
                    45.0,
                    47.5,
                    50.0,
                    52.5,
                    55.0,
                    57.5,
                    60.0,
                    62.5,
                    65.0,
                    67.5,
                    70.0,
                    72.5,
                    75.0,
                    80.0,
                    85.0,
                    90.0,
                ]
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    strikes = await tradier_client.get_option_strikes("TSLA", "2024-01-19")
    assert len(strikes) == len(mock_get("")["strikes"]["strike"])

    tradier_client.session.get.assert_called_once_with(
        "/v1/markets/options/strikes",
        params={"symbol": "TSLA", "expiration": "2024-01-19"},
    )


@pytest.mark.asyncio
async def test_get_option_strikes_invalid_date(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {"strikes": None}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    try:
        await tradier_client.get_option_strikes("TSLA", "2024/01/19")
    except InvalidExiprationDate:
        assert True


@pytest.mark.asyncio
async def test_get_option_expirations_all_info(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "expirations": {
                "expiration": [
                    {
                        "date": "2023-11-10",
                        "contract_size": 100,
                        "expiration_type": "weeklys",
                        "strikes": {"strike": [12.0, 13.0, 14.0, 15.0, 16.0, 17.0]},
                    },
                    {
                        "date": "2023-11-17",
                        "contract_size": 100,
                        "expiration_type": "standard",
                        "strikes": {
                            "strike": [9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0]
                        },
                    },
                    {
                        "date": "2023-12-29",
                        "contract_size": 100,
                        "expiration_type": "quarterlys",
                        "strikes": {
                            "strike": [12.0, 13.0, 14.0, 15.0, 15.5, 16.0, 16.5]
                        },
                    },
                ]
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    expirations = await tradier_client.get_option_expirations(
        "TSLA", strikes=True, contract_size=True, expiration_type=True
    )
    assert len(expirations) == len(mock_get("")["expirations"]["expiration"])

    for exp, exp_info in zip(expirations, mock_get("")["expirations"]["expiration"]):
        assert exp.date == exp_info["date"]
        assert exp.contract_size == exp_info["contract_size"]
        assert exp.expiration_type == exp_info["expiration_type"]
        assert exp.strikes == exp_info["strikes"]["strike"]

    tradier_client.session.get.assert_called_once_with(
        "/v1/markets/options/expirations",
        params={
            "symbol": "TSLA",
            "strikes": "true",
            "contractSize": "true",
            "expirationType": "true",
        },
    )


@pytest.mark.asyncio
async def test_get_option_expirations_only_date(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "expirations": {
                "date": [
                    "2024-01-12",
                    "2024-01-19",
                    "2024-01-26",
                    "2024-02-02",
                    "2024-02-09",
                    "2024-02-16",
                    "2024-02-23",
                    "2024-03-01",
                    "2024-03-15",
                    "2024-04-19",
                    "2024-05-17",
                    "2024-06-21",
                    "2024-07-19",
                    "2024-08-16",
                    "2024-09-20",
                    "2024-12-20",
                    "2025-01-17",
                    "2025-06-20",
                    "2025-09-19",
                    "2025-12-19",
                    "2026-01-16",
                    "2026-06-18",
                ]
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    expirations = await tradier_client.get_option_expirations("TSLA")
    assert len(expirations) == len(mock_get("")["expirations"]["date"])

    tradier_client.session.get.assert_called_once_with(
        "/v1/markets/options/expirations",
        params={
            "symbol": "TSLA",
            "strikes": "false",
            "contractSize": "false",
            "expirationType": "false",
        },
    )


@pytest.mark.asyncio
async def test_get_option_expirations_toggles(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {"expirations": None}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    # with strikes
    await tradier_client.get_option_expirations("TSLA", strikes=True)
    tradier_client.session.get.assert_called_with(
        "/v1/markets/options/expirations",
        params={
            "symbol": "TSLA",
            "strikes": "true",
            "contractSize": "false",
            "expirationType": "false",
        },
    )

    # with contract size
    await tradier_client.get_option_expirations("TSLA", contract_size=True)
    tradier_client.session.get.assert_called_with(
        "/v1/markets/options/expirations",
        params={
            "symbol": "TSLA",
            "strikes": "false",
            "contractSize": "true",
            "expirationType": "false",
        },
    )

    # with expiration type
    await tradier_client.get_option_expirations("TSLA", expiration_type=True)
    tradier_client.session.get.assert_called_with(
        "/v1/markets/options/expirations",
        params={
            "symbol": "TSLA",
            "strikes": "false",
            "contractSize": "false",
            "expirationType": "true",
        },
    )


@pytest.mark.asyncio
async def test_option_lookup(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "symbols": [
                {
                    "rootSymbol": "SPY",
                    "options": [
                        "SPY210331C00300000",
                        "SPY200702P00252000",
                        "SPY200930C00334000",
                        "SPY210115C00305000",
                        "SPY200622C00288000",
                    ],
                }
            ]
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    options = await tradier_client.option_lookup("SPY")
    assert len(options) == 5

    tradier_client.session.get.assert_called_once_with(
        "/v1/markets/options/lookup", params={"underlying": "SPY"}
    )


@pytest.mark.asyncio
async def test_option_lookup_invalid_symbol(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {"symbols": None}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    options = await tradier_client.option_lookup("SEFDF")
    assert len(options) == 0

    tradier_client.session.get.assert_called_once_with(
        "/v1/markets/options/lookup", params={"underlying": "SEFDF"}
    )


@pytest.mark.asyncio
async def test_get_user_profile(mocker, tradier_client):
    tradier_client.sandbox = False

    def mock_get(path: str, params: dict = None):
        return {
            "profile": {
                "account": [
                    {
                        "account_number": "VA000001",
                        "classification": "individual",
                        "date_created": "2016-08-01T21:08:55.000Z",
                        "day_trader": False,
                        "option_level": 6,
                        "status": "active",
                        "type": "margin",
                        "last_update_date": "2016-08-01T21:08:55.000Z",
                    },
                    {
                        "account_number": "VA000002",
                        "classification": "traditional_ira",
                        "date_created": "2016-08-05T17:24:34.000Z",
                        "day_trader": False,
                        "option_level": 3,
                        "status": "active",
                        "type": "margin",
                        "last_update_date": "2016-08-05T17:24:34.000Z",
                    },
                    {
                        "account_number": "VA000003",
                        "classification": "rollover_ira",
                        "date_created": "2016-08-01T21:08:56.000Z",
                        "day_trader": False,
                        "option_level": 2,
                        "status": "active",
                        "type": "cash",
                        "last_update_date": "2016-08-01T21:08:56.000Z",
                    },
                ],
                "id": "id-gcostanza",
                "name": "George Costanza",
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    accounts = await tradier_client.get_user_profile()

    assert len(accounts) == 3

    for account, account_info in zip(accounts, mock_get("")["profile"]["account"]):
        assert account.account_number == account_info["account_number"]
        assert account.classification == account_info["classification"]
        assert account.date_created == account_info["date_created"]
        assert account.day_trader == account_info["day_trader"]
        assert account.option_level == account_info["option_level"]
        assert account.status == account_info["status"]
        assert account.type == account_info["type"]
        assert account.last_update_date == account_info["last_update_date"]

    tradier_client.session.get.assert_called_once_with("/v1/user/profile")


@pytest.mark.asyncio
async def test_get_user_profile_sanbox(tradier_client):
    try:
        await tradier_client.get_user_profile()
    except APINotAvailable:
        assert True


@pytest.mark.asyncio
async def test_get_balance_margin(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "balances": {
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
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    balance = await tradier_client.get_balance()

    assert balance.option_short_value == 0
    assert balance.total_equity == 17798.360000000000000000000000
    assert balance.account_number == "VA00000000"
    assert balance.account_type == AccountType.margin
    assert balance.close_pl == -4813.000000000000000000
    assert balance.current_requirement == 2557.00000000000000000000
    assert balance.equity == 0
    assert balance.long_market_value == 11434.50000000000000000000
    assert balance.market_value == 11434.50000000000000000000
    assert balance.open_pl == 546.900000000000000000000000
    assert balance.option_long_value == 8877.5000000000000000000
    assert balance.option_requirement == 0
    assert balance.pending_orders_count == 0
    assert balance.short_market_value == 0
    assert balance.stock_long_value == 2557.00000000000000000000
    assert balance.total_cash == 6363.860000000000000000000000
    assert balance.uncleared_funds == 0
    assert balance.pending_cash == 0
    assert balance.margin.fed_call == 0
    assert balance.margin.maintenance_call == 0
    assert balance.margin.option_buying_power == 6363.860000000000000000000000
    assert balance.margin.stock_buying_power == 12727.7200000000000000
    assert balance.margin.stock_short_value == 0
    assert balance.margin.sweep == 0

    tradier_client.session.get.assert_called_once_with(
        f"/v1/accounts/{tradier_client.account_id}/balances"
    )


@pytest.mark.asyncio
async def test_get_balance_cash(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "balances": {
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
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    balance = await tradier_client.get_balance()

    assert balance.option_short_value == 0
    assert balance.total_equity == 17798.360000000000000000000000
    assert balance.account_number == "VA00000000"
    assert balance.account_type == AccountType.margin
    assert balance.close_pl == -4813.000000000000000000
    assert balance.current_requirement == 2557.00000000000000000000
    assert balance.equity == 0
    assert balance.long_market_value == 11434.50000000000000000000
    assert balance.market_value == 11434.50000000000000000000
    assert balance.open_pl == 546.900000000000000000000000
    assert balance.option_long_value == 8877.5000000000000000000
    assert balance.option_requirement == 0
    assert balance.pending_orders_count == 0
    assert balance.short_market_value == 0
    assert balance.stock_long_value == 2557.00000000000000000000
    assert balance.total_cash == 6363.860000000000000000000000
    assert balance.uncleared_funds == 0
    assert balance.pending_cash == 0

    assert balance.cash.cash_available == 4343.38000000
    assert balance.cash.sweep == 0
    assert balance.cash.unsettled_funds == 1310.00000000

    tradier_client.session.get.assert_called_once_with(
        f"/v1/accounts/{tradier_client.account_id}/balances"
    )


@pytest.mark.asyncio
async def test_get_balance_pdt(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "balances": {
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
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    balance = await tradier_client.get_balance()

    assert balance.option_short_value == 0
    assert balance.total_equity == 17798.360000000000000000000000
    assert balance.account_number == "VA00000000"
    assert balance.account_type == AccountType.margin
    assert balance.close_pl == -4813.000000000000000000
    assert balance.current_requirement == 2557.00000000000000000000
    assert balance.equity == 0
    assert balance.long_market_value == 11434.50000000000000000000
    assert balance.market_value == 11434.50000000000000000000
    assert balance.open_pl == 546.900000000000000000000000
    assert balance.option_long_value == 8877.5000000000000000000
    assert balance.option_requirement == 0
    assert balance.pending_orders_count == 0
    assert balance.short_market_value == 0
    assert balance.stock_long_value == 2557.00000000000000000000
    assert balance.total_cash == 6363.860000000000000000000000
    assert balance.uncleared_funds == 0
    assert balance.pending_cash == 0

    assert balance.pdt.fed_call == 0
    assert balance.pdt.maintenance_call == 0
    assert balance.pdt.option_buying_power == 6363.860000000000000000000000
    assert balance.pdt.stock_buying_power == 12727.7200000000000000
    assert balance.pdt.stock_short_value == 0

    tradier_client.session.get.assert_called_once_with(
        f"/v1/accounts/{tradier_client.account_id}/balances"
    )


@pytest.mark.asyncio
async def test_get_history_single(mocker, tradier_client):
    tradier_client.sandbox = False

    def mock_get(path: str, params: dict = None):
        return {
            "history": {
                "event": {
                    "amount": -3000.00,
                    "date": "2018-05-23T00:00:00Z",
                    "type": "journal",
                    "journal": {
                        "description": "6YA-00005 TO 6YA-00102",
                        "quantity": 0.00000000,
                    },
                }
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    history = await tradier_client.get_history()

    assert len(history) == 1


@pytest.mark.asyncio
async def test_get_history_multiple(mocker, tradier_client):
    tradier_client.sandbox = False

    def mock_get(path: str, params: dict = None):
        return {
            "history": {
                "event": [
                    {
                        "amount": -3000.00,
                        "date": "2018-05-23T00:00:00Z",
                        "type": "journal",
                        "journal": {
                            "description": "6YA-00005 TO 6YA-00102",
                            "quantity": 0.00000000,
                        },
                    },
                    {
                        "amount": 99.95,
                        "date": "2018-05-23T00:00:00Z",
                        "type": "trade",
                        "trade": {
                            "commission": 0.0000000000,
                            "description": "CALL GE     06\/22\/18    14",  # noqa
                            "price": 1.000000,
                            "quantity": -1.00000000,
                            "symbol": "GE180622C00014000",
                            "trade_type": "Option",
                        },
                    },
                ]
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    history = await tradier_client.get_history()

    assert len(history) == 2


@pytest.mark.asyncio()
async def test_get_history_page(mocker, tradier_client):
    tradier_client.sandbox = False

    def mock_get(path: str, params: dict = None):
        return {"history": {"event": []}}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    await tradier_client.get_history(page=10)

    tradier_client.session.get.assert_called_once_with(
        f"/v1/accounts/{tradier_client.account_id}/history",
        params={"page": 10, "limit": 25, "exactMatch": "false"},
    )


@pytest.mark.asyncio()
async def test_get_history_limit(mocker, tradier_client):
    tradier_client.sandbox = False

    def mock_get(path: str, params: dict = None):
        return {"history": {"event": []}}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    await tradier_client.get_history(limit=10)

    tradier_client.session.get.assert_called_once_with(
        f"/v1/accounts/{tradier_client.account_id}/history",
        params={"page": 1, "limit": 10, "exactMatch": "false"},
    )


@pytest.mark.asyncio()
async def test_get_history_exact_match(mocker, tradier_client):
    tradier_client.sandbox = False

    def mock_get(path: str, params: dict = None):
        return {"history": {"event": []}}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    await tradier_client.get_history(exact_match=True)

    tradier_client.session.get.assert_called_once_with(
        f"/v1/accounts/{tradier_client.account_id}/history",
        params={"page": 1, "limit": 25, "exactMatch": "true"},
    )


@pytest.mark.asyncio()
async def test_get_history_type(mocker, tradier_client):
    tradier_client.sandbox = False

    def mock_get(path: str, params: dict = None):
        return {"history": {"event": []}}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    await tradier_client.get_history(event_type=EventType.trade)

    for event_type in EventType:
        await tradier_client.get_history(event_type=event_type)
        tradier_client.session.get.assert_called_with(
            f"/v1/accounts/{tradier_client.account_id}/history",
            params={
                "page": 1,
                "limit": 25,
                "type": event_type.value,
                "exactMatch": "false",
            },
        )


@pytest.mark.asyncio()
async def test_get_history_start(mocker, tradier_client):
    tradier_client.sandbox = False

    def mock_get(path: str, params: dict = None):
        return {"history": {"event": []}}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    await tradier_client.get_history(start="2020-01-01")
    tradier_client.session.get.assert_called_once_with(
        f"/v1/accounts/{tradier_client.account_id}/history",
        params={
            "page": 1,
            "limit": 25,
            "start": "2020-01-01",
            "exactMatch": "false",
        },
    )

    try:
        await tradier_client.get_history(start="2020/01/01")
    except InvalidDateFormat:
        assert True


@pytest.mark.asyncio()
async def test_get_history_end(mocker, tradier_client):
    tradier_client.sandbox = False

    def mock_get(path: str, params: dict = None):
        return {"history": {"event": []}}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    await tradier_client.get_history(end="2020-01-01")
    tradier_client.session.get.assert_called_once_with(
        f"/v1/accounts/{tradier_client.account_id}/history",
        params={"page": 1, "limit": 25, "end": "2020-01-01", "exactMatch": "false"},
    )

    try:
        await tradier_client.get_history(end="2020/01/01")
    except InvalidDateFormat:
        assert True


@pytest.mark.asyncio()
async def test_get_history_symbol(mocker, tradier_client):
    tradier_client.sandbox = False

    def mock_get(path: str, params: dict = None):
        return {"history": {"event": []}}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    await tradier_client.get_history(symbol="AAPL")
    tradier_client.session.get.assert_called_once_with(
        f"/v1/accounts/{tradier_client.account_id}/history",
        params={"page": 1, "limit": 25, "symbol": "AAPL", "exactMatch": "false"},
    )


@pytest.mark.asyncio()
async def test_get_history_sanbox(mocker, tradier_client):
    tradier_client.sandbox = True

    def mock_get(path: str, params: dict = None):
        return {"history": {"event": []}}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    try:
        await tradier_client.get_history()
    except APINotAvailable:
        assert True


@pytest.mark.asyncio()
async def test_get_gainloss_single(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "gainloss": {
                "closed_position": {
                    "close_date": "2018-10-31T00:00:00.000Z",
                    "cost": 12.7,
                    "gain_loss": -2.64,
                    "gain_loss_percent": -20.7874,
                    "open_date": "2018-06-19T00:00:00.000Z",
                    "proceeds": 10.06,
                    "quantity": 1.0,
                    "symbol": "GE",
                    "term": 134,
                }
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    gainloss = await tradier_client.get_gainloss()
    assert len(gainloss) == 1

    tradier_client.session.get.assert_called_once_with(
        f"/v1/accounts/{tradier_client.account_id}/gainloss",
        params={"page": 1, "limit": 25, "sortBy": "closeDate", "sort": "desc"},
    )


@pytest.mark.asyncio()
async def test_get_gainloss_multiple(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "gainloss": {
                "closed_position": [
                    {
                        "close_date": "2018-10-31T00:00:00.000Z",
                        "cost": 12.7,
                        "gain_loss": -2.64,
                        "gain_loss_percent": -20.7874,
                        "open_date": "2018-06-19T00:00:00.000Z",
                        "proceeds": 10.06,
                        "quantity": 1.0,
                        "symbol": "GE",
                        "term": 134,
                    },
                    {
                        "close_date": "2018-10-31T00:00:00.000Z",
                        "cost": 12.7,
                        "gain_loss": -2.64,
                        "gain_loss_percent": -20.7874,
                        "open_date": "2018-06-19T00:00:00.000Z",
                        "proceeds": 10.06,
                        "quantity": 1.0,
                        "symbol": "GE",
                        "term": 134,
                    },
                ]
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    gainloss = await tradier_client.get_gainloss()
    assert len(gainloss) == 2

    tradier_client.session.get.assert_called_once_with(
        f"/v1/accounts/{tradier_client.account_id}/gainloss",
        params={"page": 1, "limit": 25, "sortBy": "closeDate", "sort": "desc"},
    )


@pytest.mark.asyncio()
async def test_get_gainloss_page(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {"gainloss": {"closed_position": []}}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    await tradier_client.get_gainloss(page=10)

    tradier_client.session.get.assert_called_once_with(
        f"/v1/accounts/{tradier_client.account_id}/gainloss",
        params={"page": 10, "limit": 25, "sortBy": "closeDate", "sort": "desc"},
    )


@pytest.mark.asyncio()
async def test_get_gainloss_limit(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {"gainloss": {"closed_position": []}}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)
    await tradier_client.get_gainloss(limit=10)

    tradier_client.session.get.assert_called_once_with(
        f"/v1/accounts/{tradier_client.account_id}/gainloss",
        params={"page": 1, "limit": 10, "sortBy": "closeDate", "sort": "desc"},
    )


@pytest.mark.asyncio()
async def test_get_gainloss_sort_by(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {"gainloss": {"closed_position": []}}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    await tradier_client.get_gainloss(sort_by_close_date=True)
    tradier_client.session.get.assert_called_with(
        f"/v1/accounts/{tradier_client.account_id}/gainloss",
        params={
            "page": 1,
            "limit": 25,
            "sortBy": "closeDate",
            "sort": "desc",
        },
    )

    await tradier_client.get_gainloss(sort_by_close_date=False)
    tradier_client.session.get.assert_called_with(
        f"/v1/accounts/{tradier_client.account_id}/gainloss",
        params={
            "page": 1,
            "limit": 25,
            "sortBy": "openDate",
            "sort": "desc",
        },
    )


@pytest.mark.asyncio()
async def test_get_gainloss_sort(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {"gainloss": {"closed_position": []}}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    await tradier_client.get_gainloss(desc=True)
    tradier_client.session.get.assert_called_with(
        f"/v1/accounts/{tradier_client.account_id}/gainloss",
        params={
            "page": 1,
            "limit": 25,
            "sortBy": "closeDate",
            "sort": "desc",
        },
    )

    await tradier_client.get_gainloss(desc=False)
    tradier_client.session.get.assert_called_with(
        f"/v1/accounts/{tradier_client.account_id}/gainloss",
        params={
            "page": 1,
            "limit": 25,
            "sortBy": "closeDate",
            "sort": "asc",
        },
    )


@pytest.mark.asyncio()
async def test_get_gainloss_start(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {"gainloss": {"closed_position": []}}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    await tradier_client.get_gainloss(start="2020-01-01")
    tradier_client.session.get.assert_called_once_with(
        f"/v1/accounts/{tradier_client.account_id}/gainloss",
        params={
            "page": 1,
            "limit": 25,
            "sortBy": "closeDate",
            "sort": "desc",
            "start": "2020-01-01",
        },
    )

    try:
        await tradier_client.get_gainloss(start="2020/01/01")
    except InvalidDateFormat:
        assert True


@pytest.mark.asyncio()
async def test_get_gainloss_end(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {"gainloss": {"closed_position": []}}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    await tradier_client.get_gainloss(end="2020-01-01")
    tradier_client.session.get.assert_called_once_with(
        f"/v1/accounts/{tradier_client.account_id}/gainloss",
        params={
            "page": 1,
            "limit": 25,
            "sortBy": "closeDate",
            "sort": "desc",
            "end": "2020-01-01",
        },
    )

    try:
        await tradier_client.get_gainloss(end="2020/01/01")
    except InvalidDateFormat:
        assert True


@pytest.mark.asyncio()
async def test_get_gainloss_symbol(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {"gainloss": {"closed_position": []}}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    await tradier_client.get_gainloss(symbol="AAPL")
    tradier_client.session.get.assert_called_once_with(
        f"/v1/accounts/{tradier_client.account_id}/gainloss",
        params={
            "page": 1,
            "limit": 25,
            "sortBy": "closeDate",
            "sort": "desc",
            "symbol": "AAPL",
        },
    )


@pytest.mark.asyncio()
async def test_get_calendar(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {
            "calendar": {
                "month": 1,
                "year": 2024,
                "days": {
                    "day": [
                        {
                            "date": "2024-01-01",
                            "status": "closed",
                            "description": "Market is closed for New Years Day",
                        },
                        {
                            "date": "2024-01-02",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-03",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-04",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-05",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-06",
                            "status": "closed",
                            "description": "Market is closed",
                        },
                        {
                            "date": "2024-01-07",
                            "status": "closed",
                            "description": "Market is closed",
                        },
                        {
                            "date": "2024-01-08",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-09",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-10",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-11",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-12",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-13",
                            "status": "closed",
                            "description": "Market is closed",
                        },
                        {
                            "date": "2024-01-14",
                            "status": "closed",
                            "description": "Market is closed",
                        },
                        {
                            "date": "2024-01-15",
                            "status": "closed",
                            "description": "Market is closed for Martin Luther King, Jr. Day",
                        },
                        {
                            "date": "2024-01-16",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-17",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-18",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-19",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-20",
                            "status": "closed",
                            "description": "Market is closed",
                        },
                        {
                            "date": "2024-01-21",
                            "status": "closed",
                            "description": "Market is closed",
                        },
                        {
                            "date": "2024-01-22",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-23",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-24",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-25",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-26",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-27",
                            "status": "closed",
                            "description": "Market is closed",
                        },
                        {
                            "date": "2024-01-28",
                            "status": "closed",
                            "description": "Market is closed",
                        },
                        {
                            "date": "2024-01-29",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-30",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                        {
                            "date": "2024-01-31",
                            "status": "open",
                            "description": "Market is open",
                            "premarket": {"start": "07:00", "end": "09:24"},
                            "open": {"start": "09:30", "end": "16:00"},
                            "postmarket": {"start": "16:00", "end": "19:55"},
                        },
                    ]
                },
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    calendar = await tradier_client.get_calendar("2024", "01")
    assert len(calendar) == 31

    tradier_client.session.get.assert_called_once_with(
        "/v1/markets/calendar",
        params={"year": "2024", "month": "01"},
    )


@pytest.mark.asyncio()
async def test_get_calendar_invalid_param(mocker, tradier_client):
    def mock_get(path: str, params: dict = None):
        return {}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    try:
        await tradier_client.get_calendar("24", "13")
    except InvalidParameter:
        assert True

    try:
        await tradier_client.get_calendar("2024", "1")
    except InvalidParameter:
        assert True

    try:
        await tradier_client.get_calendar("2024", "13")
    except InvalidParameter:
        assert True


@pytest.mark.asyncio()
async def test_buy_stock_market_order(mocker, tradier_client):
    def mock_post(path: str, data: dict = None):
        return {
            "order": {
                "id": 257459,
                "status": "ok",
                "partner_id": "c4998eb7-06e8-4820-a7ab-55d9760065fb",
            }
        }

    mocker.patch.object(tradier_client.session, "post", side_effect=mock_post)

    await tradier_client.buy_stock("AAPL", 100)

    tradier_client.session.post.assert_called_once_with(
        "/v1/accounts/account_id/orders",
        data={
            "class": "equity",
            "symbol": "AAPL",
            "side": "buy",
            "quantity": "100",
            "type": "market",
            "duration": "day",
            "price": "",
            "stop": "",
            "tag": None,
        },
    )


@pytest.mark.asyncio()
async def test_buy_stock_limit_order(mocker, tradier_client):
    def mock_post(path: str, data: dict = None):
        return {
            "order": {
                "id": 257459,
                "status": "ok",
                "partner_id": "c4998eb7-06e8-4820-a7ab-55d9760065fb",
            }
        }

    mocker.patch.object(tradier_client.session, "post", side_effect=mock_post)

    await tradier_client.buy_stock("AAPL", 100, OrderType.limit, price=100.1)

    tradier_client.session.post.assert_called_once_with(
        "/v1/accounts/account_id/orders",
        data={
            "class": "equity",
            "symbol": "AAPL",
            "side": "buy",
            "quantity": "100",
            "type": "limit",
            "duration": "day",
            "price": "100.1",
            "stop": "",
            "tag": None,
        },
    )


@pytest.mark.asyncio()
async def test_buy_stock_limit_order_no_price(mocker, tradier_client):
    def mock_post(path: str, data: dict = None):
        return {
            "order": {
                "id": 257459,
                "status": "ok",
                "partner_id": "c4998eb7-06e8-4820-a7ab-55d9760065fb",
            }
        }

    mocker.patch.object(tradier_client.session, "post", side_effect=mock_post)
    try:
        await tradier_client.buy_stock("AAPL", 100, OrderType.limit)
    except MissingRequiredParameter:
        assert True

    tradier_client.session.post.assert_not_called()


@pytest.mark.asyncio()
async def test_buy_stock_stop_order(mocker, tradier_client):
    def mock_post(path: str, data: dict = None):
        return {
            "order": {
                "id": 257459,
                "status": "ok",
                "partner_id": "c4998eb7-06e8-4820-a7ab-55d9760065fb",
            }
        }

    mocker.patch.object(tradier_client.session, "post", side_effect=mock_post)

    await tradier_client.buy_stock("AAPL", 100, OrderType.stop, stop=100.1)

    tradier_client.session.post.assert_called_once_with(
        "/v1/accounts/account_id/orders",
        data={
            "class": "equity",
            "symbol": "AAPL",
            "side": "buy",
            "quantity": "100",
            "type": "stop",
            "duration": "day",
            "price": "",
            "stop": "100.1",
            "tag": None,
        },
    )


@pytest.mark.asyncio()
async def test_buy_stock_stop_no_stop(mocker, tradier_client):
    def mock_post(path: str, data: dict = None):
        return {
            "order": {
                "id": 257459,
                "status": "ok",
                "partner_id": "c4998eb7-06e8-4820-a7ab-55d9760065fb",
            }
        }

    mocker.patch.object(tradier_client.session, "post", side_effect=mock_post)
    try:
        await tradier_client.buy_stock("AAPL", 100, OrderType.stop)
    except MissingRequiredParameter:
        assert True

    tradier_client.session.post.assert_not_called()


@pytest.mark.asyncio()
async def test_sell_stock_market_order(mocker, tradier_client):
    def mock_post(path: str, data: dict = None):
        return {
            "order": {
                "id": 257459,
                "status": "ok",
                "partner_id": "c4998eb7-06e8-4820-a7ab-55d9760065fb",
            }
        }

    mocker.patch.object(tradier_client.session, "post", side_effect=mock_post)

    await tradier_client.sell_stock("AAPL", 100)

    tradier_client.session.post.assert_called_once_with(
        "/v1/accounts/account_id/orders",
        data={
            "class": "equity",
            "symbol": "AAPL",
            "side": "sell",
            "quantity": "100",
            "type": "market",
            "duration": "day",
            "price": "",
            "stop": "",
            "tag": None,
        },
    )


@pytest.mark.asyncio()
async def test_sell_stock_limit_order(mocker, tradier_client):
    def mock_post(path: str, data: dict = None):
        return {
            "order": {
                "id": 257459,
                "status": "ok",
                "partner_id": "c4998eb7-06e8-4820-a7ab-55d9760065fb",
            }
        }

    mocker.patch.object(tradier_client.session, "post", side_effect=mock_post)

    await tradier_client.sell_stock("AAPL", 100, OrderType.limit, price=100.1)

    tradier_client.session.post.assert_called_once_with(
        "/v1/accounts/account_id/orders",
        data={
            "class": "equity",
            "symbol": "AAPL",
            "side": "sell",
            "quantity": "100",
            "type": "limit",
            "duration": "day",
            "price": "100.1",
            "stop": "",
            "tag": None,
        },
    )


@pytest.mark.asyncio()
async def test_sell_stock_limit_order_no_price(mocker, tradier_client):
    def mock_post(path: str, data: dict = None):
        return {
            "order": {
                "id": 257459,
                "status": "ok",
                "partner_id": "c4998eb7-06e8-4820-a7ab-55d9760065fb",
            }
        }

    mocker.patch.object(tradier_client.session, "post", side_effect=mock_post)
    try:
        await tradier_client.sell_stock("AAPL", 100, OrderType.limit)
    except MissingRequiredParameter:
        assert True

    tradier_client.session.post.assert_not_called()


@pytest.mark.asyncio()
async def test_sell_stock_stop_order(mocker, tradier_client):
    def mock_post(path: str, data: dict = None):
        return {
            "order": {
                "id": 257459,
                "status": "ok",
                "partner_id": "c4998eb7-06e8-4820-a7ab-55d9760065fb",
            }
        }

    mocker.patch.object(tradier_client.session, "post", side_effect=mock_post)

    await tradier_client.sell_stock("AAPL", 100, OrderType.stop, stop=100.1)

    tradier_client.session.post.assert_called_once_with(
        "/v1/accounts/account_id/orders",
        data={
            "class": "equity",
            "symbol": "AAPL",
            "side": "sell",
            "quantity": "100",
            "type": "stop",
            "duration": "day",
            "price": "",
            "stop": "100.1",
            "tag": None,
        },
    )


@pytest.mark.asyncio()
async def test_sell_stock_stop_no_stop(mocker, tradier_client):
    def mock_post(path: str, data: dict = None):
        return {
            "order": {
                "id": 257459,
                "status": "ok",
                "partner_id": "c4998eb7-06e8-4820-a7ab-55d9760065fb",
            }
        }

    mocker.patch.object(tradier_client.session, "post", side_effect=mock_post)
    try:
        await tradier_client.sell_stock("AAPL", 100, OrderType.stop)
    except MissingRequiredParameter:
        assert True

    tradier_client.session.post.assert_not_called()


@pytest.mark.asyncio()
async def test_get_streaming_market_data_session(mocker, tradier_client):
    def mock_post(path: str, data: dict = None):
        return {
            "stream": {
                "url": "https://stream.tradier.com/v1/markets/events",
                "sessionid": "c8638963-a6d4-4fb9-9bc6-e25fbd8c60c3",
            }
        }

    mocker.patch.object(tradier_client.session, "post", side_effect=mock_post)

    await tradier_client._get_streaming_market_data_session()

    tradier_client.session.post.assert_called_once_with("/v1/markets/events/session")


@pytest.mark.asyncio()
async def test_get_streaming_account_session(mocker, tradier_client):
    def mock_post(path: str, data: dict = None):
        return {
            "stream": {
                "url": "wss://ws.tradier.com/v1/accounts/events",
                "sessionid": "c8638963-a6d4-4fb9-9bc6-e25fbd8c60c3",
            }
        }

    mocker.patch.object(tradier_client.session, "post", side_effect=mock_post)

    await tradier_client._get_streaming_account_session()

    tradier_client.session.post.assert_called_once_with("/v1/accounts/events/session")


@pytest.mark.asyncio()
async def test_get_historical_quotes(mocker, tradier_client):
    def mock_get(url: str, params: dict = None):
        return {
            "history": {
                "day": [
                    {
                        "date": "2019-01-02",
                        "open": 154.89,
                        "high": 158.85,
                        "low": 154.23,
                        "close": 157.92,
                        "volume": 37039737,
                    },
                    {
                        "date": "2019-01-03",
                        "open": 143.98,
                        "high": 145.72,
                        "low": 142.0,
                        "close": 142.19,
                        "volume": 91312195,
                    },
                    {
                        "date": "2019-01-04",
                        "open": 144.53,
                        "high": 148.5499,
                        "low": 143.8,
                        "close": 148.26,
                        "volume": 58607070,
                    },
                ]
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    quotes = await tradier_client.get_historical_quotes(
        "AAPL", "daily", "2019-01-01", "2019-01-05"
    )

    assert len(quotes) == 3

    tradier_client.session.get.assert_called_once_with(
        "/v1/markets/history",
        params={
            "symbol": "AAPL",
            "interval": "daily",
            "start": "2019-01-01",
            "end": "2019-01-05",
        },
    )


@pytest.mark.asyncio()
async def test_get_historical_quotes_invalid_param(mocker, tradier_client):
    def mock_get(url: str, params: dict = None):
        return {}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    try:
        await tradier_client.get_historical_quotes(
            "AAPL", "daily", "20190101", "2019-01-01"
        )
    except InvalidParameter:
        assert True

    try:
        await tradier_client.get_historical_quotes(
            "AAPL", "daily", "2019-01-01", "20190102"
        )
    except InvalidParameter:
        assert True

    try:
        await tradier_client.get_historical_quotes(
            "AAPL", "hourly", "2019-01-01", "2019-01-01"
        )

    except InvalidParameter:
        assert True

    tradier_client.session.get.assert_not_called()


@pytest.mark.asyncio()
async def test_get_historical_quotes_non_list(mocker, tradier_client):
    def mock_get(url: str, params: dict = None):
        return {
            "history": {
                "day": {
                    "date": "2019-01-02",
                    "open": 154.89,
                    "high": 158.85,
                    "low": 154.23,
                    "close": 157.92,
                    "volume": 37039737,
                }
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    response = await tradier_client.get_historical_quotes(
        "AAPL", "daily", "2019-01-01", "2019-01-05"
    )

    assert len(response) == 1


@pytest.mark.asyncio()
async def test_get_time_and_sale(mocker, tradier_client):
    def mock_get(url: str, params: dict = None):
        return {
            "series": {
                "data": [
                    {
                        "time": "2019-05-09T09:30:00",
                        "timestamp": 1557408600,
                        "price": 199.64499999999998,
                        "open": 200.46,
                        "high": 200.53,
                        "low": 198.76,
                        "close": 200.1154,
                        "volume": 1273841,
                        "vwap": 199.77806,
                    },
                    {
                        "time": "2019-05-09T09:31:00",
                        "timestamp": 1557408660,
                        "price": 200.2,
                        "open": 200.15,
                        "high": 200.54,
                        "low": 199.86,
                        "close": 200.49,
                        "volume": 228068,
                        "vwap": 200.17588,
                    },
                    {
                        "time": "2019-05-09T09:32:00",
                        "timestamp": 1557408720,
                        "price": 200.445,
                        "open": 200.51,
                        "high": 200.75,
                        "low": 200.14,
                        "close": 200.2,
                        "volume": 277041,
                        "vwap": 200.44681,
                    },
                ]
            }
        }

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    response = await tradier_client.get_time_and_sales("AAPL")

    assert len(response) == 3

    tradier_client.session.get.assert_called_once_with(
        "/v1/markets/timesales",
        params={
            "symbol": "AAPL",
            "interval": "tick",
            "start": None,
            "end": None,
            "session_filter": "all",
        },
    )


@pytest.mark.asyncio()
async def test_get_time_sale_invalid_param(mocker, tradier_client):
    def mock_get(url: str, params: dict = None):
        return {}

    mocker.patch.object(tradier_client.session, "get", side_effect=mock_get)

    try:
        await tradier_client.get_time_and_sales("AAPL", interval="hourly")
    except InvalidParameter:
        assert True

    try:
        await tradier_client.get_time_and_sales("AAPL", session_filter="pre")
    except InvalidParameter:
        assert True

    try:
        await tradier_client.get_time_and_sales("AAPL", start="2019-01-01")
    except InvalidParameter:
        assert True

    try:
        await tradier_client.get_time_and_sales("AAPL", end="2019-01-01")
    except InvalidParameter:
        assert True

    tradier_client.session.get.assert_not_called()
