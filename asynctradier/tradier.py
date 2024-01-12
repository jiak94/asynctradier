import json
from typing import AsyncIterator, List, Optional

import websockets

from asynctradier.common import Duration, OptionType, OrderClass, OrderSide, OrderType
from asynctradier.common.option_contract import OptionContract
from asynctradier.common.order import Order
from asynctradier.common.position import Position
from asynctradier.common.quote import Quote
from asynctradier.exceptions import (
    InvalidExiprationDate,
    InvalidOptionType,
    InvalidParameter,
    InvalidStrikeType,
    MissingRequiredParameter,
)
from asynctradier.utils.common import build_option_symbol, is_valid_expiration_date

from .utils.webutils import WebUtil


class TradierClient:
    """
    A client for interacting with the Tradier API.

    Args:
        account_id (str): The account ID.
        token (str): The API token.
        sandbox (bool, optional): Whether to use the sandbox environment. Defaults to False.
    """

    def __init__(self, account_id: str, token: str, sandbox: bool = False) -> None:
        self.account_id = account_id
        self.token = token
        base_url = (
            "https://api.tradier.com" if not sandbox else "https://sandbox.tradier.com"
        )
        self.session = WebUtil(base_url, token)

    async def get_positions(self) -> List[Position]:
        """
        Get the positions for the account.

        Returns:
            List[Position]: A list of Position objects.
        """
        url = f"/v1/accounts/{self.account_id}/positions"
        response = await self.session.get(url)
        if response["positions"] == "null":
            positions = []
        else:
            positions = response["positions"]["position"]
        if not isinstance(positions, list):
            positions = [positions]
        results: List[Position] = []
        for position in positions:
            results.append(
                Position(
                    **position,
                )
            )
        return results

    async def get_order(self, order_id: str) -> Order:
        """
        Get an order by its ID.

        Args:
            order_id (str): The ID of the order.

        Returns:
            Order: The Order object.
        """
        url = f"/v1/accounts/{self.account_id}/orders/{order_id}"
        params = {"includeTags": "true"}
        response = await self.session.get(url, params=params)
        order = response["order"]
        return Order(
            **order,
        )

    async def buy_option(
        self,
        symbol: str,
        expiration_date: str,
        strike: float | int,
        option_type: OptionType,
        quantity: int,
        order_type: OrderType = OrderType.market,
        order_duration: Duration = Duration.day,
        tag: Optional[str] = None,
        price: Optional[float] = None,
        stop: Optional[float] = None,
    ) -> Order:
        """
        Place a buy option order.

        Args:
            symbol (str): The symbol of the option.
            expiration_date (str): The expiration date of the option (YYYY-MM-DD).
            strike (float | int): The strike price of the option.
            option_type (OptionType): The type of the option (call or put).
            quantity (int): The quantity of the option contracts to buy.
            order_type (OrderType, optional): The type of the order. Defaults to OrderType.market.
            order_duration (Duration, optional): The duration of the order. Defaults to Duration.day.
            tag (str, optional): An optional tag for the order. Defaults to None.
            price (float, optional): The price at which to place the order. Required for limit orders. Defaults to None.
            stop (float, optional): The stop price for the order. Required for stop orders. Defaults to None.

        Returns:
            Order: The Order object.
        """
        return await self._option_operation(
            OrderSide.buy_to_open,
            symbol,
            expiration_date,
            strike,
            option_type,
            quantity,
            order_type,
            order_duration,
            tag,
            price,
            stop,
        )

    async def sell_option(
        self,
        symbol: str,
        expiration_date: str,
        strike: float | int,
        option_type: OptionType,
        quantity: int,
        order_type: OrderType = OrderType.market,
        order_duration: Duration = Duration.day,
        tag: Optional[str] = None,
        price: Optional[float] = None,
        stop: Optional[float] = None,
    ) -> Order:
        """
        Place a sell option order.

        Args:
            symbol (str): The symbol of the option.
            expiration_date (str): The expiration date of the option (YYYY-MM-DD).
            strike (float | int): The strike price of the option.
            option_type (OptionType): The type of the option (call or put).
            quantity (int): The quantity of the option contracts to sell.
            order_type (OrderType, optional): The type of the order. Defaults to OrderType.market.
            order_duration (Duration, optional): The duration of the order. Defaults to Duration.day.
            tag (str, optional): An optional tag for the order. Defaults to None.
            price (float, optional): The price at which to place the order. Required for limit orders. Defaults to None.
            stop (float, optional): The stop price for the order. Required for stop orders. Defaults to None.

        Returns:
            Order: The Order object.
        """
        return await self._option_operation(
            OrderSide.sell_to_close,
            symbol,
            expiration_date,
            strike,
            option_type,
            quantity,
            order_type,
            order_duration,
            tag,
            price,
            stop,
        )

    async def _option_operation(
        self,
        side: OrderSide,
        symbol: str,
        expiration_date: str,
        strike: float | int,
        option_type: OptionType,
        quantity: int,
        order_type: OrderType = OrderType.market,
        order_duration: Duration = Duration.day,
        tag: Optional[str] = None,
        price: Optional[float] = None,
        stop: Optional[float] = None,
    ) -> Order:
        """
        Perform an option operation.

        Args:
            side (OrderSide): The side of the option order.
            symbol (str): The symbol of the option.
            expiration_date (str): The expiration date of the option (YYYY-MM-DD).
            strike (float | int): The strike price of the option.
            option_type (OptionType): The type of the option (call or put).
            quantity (int): The quantity of the option contracts.
            order_type (OrderType, optional): The type of the order. Defaults to OrderType.market.
            order_duration (Duration, optional): The duration of the order. Defaults to Duration.day.
            tag (str, optional): An optional tag for the order. Defaults to None.
            price (float, optional): The price at which to place the order. Required for limit orders. Defaults to None.
            stop (float, optional): The stop price for the order. Required for stop orders. Defaults to None.

        Returns:
            Order: The Order object.
        """
        if not is_valid_expiration_date(expiration_date):
            raise InvalidExiprationDate(expiration_date)

        if not isinstance(option_type, OptionType):
            raise InvalidOptionType(option_type)

        if not isinstance(strike, float) and not isinstance(strike, int):
            raise InvalidStrikeType(strike)

        if order_type == OrderType.limit and price is None:
            raise MissingRequiredParameter("Price must be specified for limit orders")

        if order_type == OrderType.stop and stop is None:
            raise MissingRequiredParameter("Stop must be specified for stop orders")

        url = f"/v1/accounts/{self.account_id}/orders"
        params = {
            "class": OrderClass.option.value,
            "symbol": symbol,
            "option_symbol": build_option_symbol(
                symbol, expiration_date, strike, option_type.value
            ),
            "side": side.value,
            "quantity": str(quantity),
            "type": order_type.value,
            "duration": order_duration.value,
            "price": price if price is not None else "",
            "stop": stop if stop is not None else "",
            "tag": tag,
        }
        response = await self.session.post(url, data=params)
        order = response["order"]
        return Order(
            **order,
        )

    async def cancel_order(self, order_id: str | int) -> Order:
        """
        Cancel an order by its ID.

        Args:
            order_id (str | int): The ID of the order.

        Returns:
            Order: The Order object.
        """
        url = f"/v1/accounts/{self.account_id}/orders/{order_id}"
        response = await self.session.delete(url)
        order = response["order"]
        return Order(
            **order,
        )

    async def get_orders(self, page: int = 1) -> List[Order]:
        """
        Get a list of orders for the account.

        Parameters:
            page (int, optional): The page number of the orders to retrieve. Defaults to 1.

        Returns:
            List[Order]: A list of Order objects.
        """
        res = []
        page = 1
        while True:
            orders = await self._get_orders(page)
            res += orders
            page += 1
            if len(orders) <= 0:
                break
        return res

    async def _get_orders(self, page: int) -> List[Order]:
        """
        Get a list of orders for the account.

        Args:
            page (int): The page number of the orders to retrieve.

        Returns:
            List[Order]: A list of Order objects.
        """
        url = f"/v1/accounts/{self.account_id}/orders"
        params = {
            "page": page,
            "includeTags": "true",
        }
        response = await self.session.get(url, params=params)
        if response["orders"] == "null":
            orders = []
        else:
            orders = response["orders"]["order"]

        if not isinstance(orders, list):
            orders = [orders]
        results: List[Order] = []
        for order in orders:
            results.append(
                Order(
                    **order,
                )
            )
        return results

    async def modify_order(
        self,
        order_id: str | int,
        order_type: Optional[OrderType] = None,
        order_duration: Optional[Duration] = None,
        price: Optional[float] = None,
        stop: Optional[float] = None,
    ) -> Order:
        """
        Modify an order by its ID.

        Args:
            order_id (str | int): The ID of the order.
            order_type (OrderType, optional): The new type of the order. Defaults to None.
            order_duration (Duration, optional): The new duration of the order. Defaults to None.
            price (float, optional): The new price for the order. Defaults to None.
            stop (float, optional): The new stop price for the order. Defaults to None.

        Returns:
            Order: The Order object.
        """
        url = f"/v1/accounts/{self.account_id}/orders/{order_id}"
        param = {}
        if order_type is not None:
            param["type"] = order_type.value
        if order_duration is not None:
            param["duration"] = order_duration.value
        if price is not None:
            param["price"] = price
        if stop is not None:
            param["stop"] = stop

        if len(param) == 0:
            raise InvalidParameter("No parameters to modify")
        response = await self.session.put(url, data=param)
        order = response["order"]
        return Order(
            **order,
        )

    async def _get_streaming_account_session(self) -> str:
        """
        Get the streaming account session.

        Returns:
            str: The streaming account session.
        """
        url = "/v1/accounts/events/session"
        response = await self.session.post(url)
        return response

    async def stream_order(self, with_detail: bool = True) -> AsyncIterator[Order]:
        """
        Stream order events.

        Args:
            with_detail (bool, optional): Whether to include order details. Defaults to True.
        """
        streaming_session = await self._get_streaming_account_session()
        uri = streaming_session["stream"]["url"]
        session_id = streaming_session["stream"]["sessionid"]

        async with websockets.connect(uri) as websocket:
            payload = {
                "events": ["order"],
                "sessionid": session_id,
                "excludeAccounts": [],
            }
            payload = json.dumps(payload)

            await websocket.send(payload)

            while True:
                response = json.loads(await websocket.recv())
                if response["event"] == "heartbeat":
                    continue
                if response["event"] == "order":
                    if with_detail:
                        order_id = response["id"]
                        yield await self.get_order(order_id)
                    else:
                        yield response

    async def multileg(
        self,
        symbol: str,
        order_type: OrderType,
        duration: Duration,
        legs: List[OptionContract],
        price: Optional[float] = None,
    ) -> Order:
        """
        Executes a multileg order.

        Args:
            symbol (str): The symbol of the order.
            order_type (OrderType): The type of the order.
            duration (Duration): The duration of the order.
            legs (List[OptionContract]): The list of option contracts for the multileg order.
            price (Optional[float]): The price of the order (required for spread orders).

        Returns:
            Order: The executed order.

        Raises:
            MissingRequiredParameter: If price is not specified for spread orders.
        """

        url = f"/v1/accounts/{self.account_id}/orders"
        body = {}
        if order_type == OrderType.debit or order_type == OrderType.credit:
            if price is None:
                raise MissingRequiredParameter(
                    "Price must be specified for spread orders"
                )
            body["price"] = price

        body["class"] = OrderClass.multileg.value
        body["symbol"] = symbol
        body["type"] = order_type.value
        body["duration"] = duration.value

        for i, leg in enumerate(legs):
            body[f"option_symbol[{i}]"] = leg.option_symbol
            body[f"quantity[{i}]"] = str(leg.quantity)
            body[f"side[{i}]"] = leg.order_side.value

        response = await self.session.post(url, data=body)
        order = response["order"]
        return Order(
            **order,
        )

    async def get_quotes(self, symbols: List[str], greeks: bool = False) -> List[Quote]:
        """
        Get quotes for a list of symbols.

        Args:
            symbols (List[str]): A list of symbols.
            greeks (bool, optional): Whether to include greeks in the response. Defaults to False.
        """
        url = "/v1/markets/quotes"
        params = {"symbols": ",".join(symbols), "greeks": str(greeks).lower()}

        response = await self.session.get(url, params=params)

        quotes = response.get("quotes", {}).get("quote", [])
        results = []
        if not isinstance(quotes, list):
            quotes = [quotes]
        for quote in quotes:
            results.append(
                Quote(
                    **quote,
                )
            )
        unmatch_symbols = (
            response.get("quotes", {}).get("unmatched_symbols", {}).get("symbol", [])
        )
        if not isinstance(unmatch_symbols, list):
            unmatch_symbols = [unmatch_symbols]

        for symbol in unmatch_symbols:
            results.append(
                Quote(
                    symbol=symbol,
                    note="unmatched symbol",
                )
            )
        return results

    async def get_option_chains(
        self,
        symbol: str,
        expiration_date: str,
        greeks: bool = False,
        option_type: Optional[OptionType] = None,
    ) -> List[Quote]:
        """
        Get option chains for a symbol.

        Args:
            symbol (str): The symbol.
            expiration_date (str): The expiration date (YYYY-MM-DD).
            greeks (bool, optional): Whether to include greeks in the response. Defaults to False.
        """
        if not is_valid_expiration_date(expiration_date):
            raise InvalidExiprationDate(expiration_date)

        url = "/v1/markets/options/chains"
        params = {
            "symbol": symbol,
            "expiration": expiration_date,
            "greeks": str(greeks).lower(),
        }
        response = await self.session.get(url, params=params)

        # if no options or options is None, return empty list
        if response.get("options") is None:
            return []
        results = []
        chains = response.get("options", {}).get("option", [])
        if not isinstance(chains, list):
            chains = [chains]
        for chain in chains:
            if option_type is not None and chain["option_type"] != option_type.value:
                continue
            results.append(
                Quote(
                    **chain,
                )
            )
        return results
