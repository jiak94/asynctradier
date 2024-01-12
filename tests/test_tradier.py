from unittest.mock import call

import pytest

from asynctradier.common import Duration, OptionType, OrderSide, OrderType
from asynctradier.common.option_contract import OptionContract
from asynctradier.exceptions import InvalidExiprationDate
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
                    1.67,
                    3.33,
                    5.0,
                    6.67,
                    8.33,
                    10.0,
                    11.67,
                    13.33,
                    15.0,
                    16.67,
                    18.33,
                    20.0,
                    21.67,
                    23.33,
                    25.0,
                    26.67,
                    28.33,
                    30.0,
                    31.67,
                    33.33,
                    50.0,
                    55.0,
                    60.0,
                    65.0,
                    66.67,
                    70.0,
                    75.0,
                    80.0,
                    83.33,
                    85.0,
                    90.0,
                    95.0,
                    100.0,
                    105.0,
                    110.0,
                    115.0,
                    116.67,
                    120.0,
                    123.33,
                    125.0,
                    126.67,
                    130.0,
                    133.33,
                    135.0,
                    136.67,
                    140.0,
                    143.33,
                    145.0,
                    146.67,
                    150.0,
                    153.33,
                    155.0,
                    156.67,
                    160.0,
                    163.33,
                    165.0,
                    166.67,
                    170.0,
                    173.33,
                    175.0,
                    176.67,
                    180.0,
                    183.33,
                    185.0,
                    186.67,
                    190.0,
                    193.33,
                    195.0,
                    200.0,
                    203.33,
                    205.0,
                    206.67,
                    207.5,
                    210.0,
                    212.5,
                    213.33,
                    215.0,
                    216.67,
                    217.5,
                    220.0,
                    222.5,
                    223.33,
                    225.0,
                    226.67,
                    227.5,
                    230.0,
                    232.5,
                    233.33,
                    235.0,
                    236.67,
                    237.5,
                    240.0,
                    242.5,
                    243.33,
                    245.0,
                    246.67,
                    247.5,
                    250.0,
                    252.5,
                    253.33,
                    255.0,
                    256.67,
                    257.5,
                    260.0,
                    262.5,
                    263.33,
                    265.0,
                    266.67,
                    267.5,
                    270.0,
                    272.5,
                    273.33,
                    275.0,
                    276.67,
                    277.5,
                    280.0,
                    282.5,
                    283.33,
                    285.0,
                    286.67,
                    287.5,
                    290.0,
                    293.33,
                    295.0,
                    296.67,
                    300.0,
                    303.33,
                    305.0,
                    306.67,
                    310.0,
                    313.33,
                    315.0,
                    316.67,
                    320.0,
                    323.33,
                    325.0,
                    326.67,
                    330.0,
                    333.33,
                    335.0,
                    336.67,
                    340.0,
                    341.67,
                    343.33,
                    345.0,
                    346.67,
                    350.0,
                    353.33,
                    355.0,
                    356.67,
                    358.33,
                    360.0,
                    363.33,
                    365.0,
                    366.67,
                    370.0,
                    373.33,
                    375.0,
                    376.67,
                    380.0,
                    383.33,
                    385.0,
                    386.67,
                    390.0,
                    391.67,
                    393.33,
                    396.67,
                    400.0,
                    408.33,
                    410.0,
                    416.67,
                    420.0,
                    425.0,
                    433.33,
                    440.0,
                    441.67,
                    450.0,
                    458.33,
                    466.67,
                    475.0,
                    483.33,
                    491.67,
                    500.0,
                    510.0,
                    516.67,
                    520.0,
                    530.0,
                    533.33,
                    540.0,
                    550.0,
                    558.33,
                    560.0,
                    566.67,
                    575.0,
                    583.33,
                    591.67,
                    600.0,
                    608.33,
                    616.67,
                    625.0,
                    633.33,
                    641.67,
                    650.0,
                    666.67,
                    675.0,
                    683.33,
                    691.67,
                    700.0,
                    708.33,
                    716.67,
                    725.0,
                    733.33,
                    741.67,
                    750.0,
                    758.33,
                    766.67,
                    775.0,
                    783.33,
                    791.67,
                    800.0,
                    808.33,
                    816.67,
                    825.0,
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
