from unittest.mock import call

import pytest

from asynctradier.common import Duration, OptionOrderSide, OrderType
from asynctradier.common.option_contract import OptionContract
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
    positions = [p async for p in tradier_client.get_positions()]
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
    positions = [p async for p in tradier_client.get_positions()]
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
        "call",
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
        "call",
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
            "call",
            OptionOrderSide.buy_to_open,
            1,
        ),
        OptionContract(
            "SPY",
            "2019-03-29",
            270.00,
            "put",
            OptionOrderSide.buy_to_open,
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
