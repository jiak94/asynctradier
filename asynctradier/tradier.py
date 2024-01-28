import json
from typing import AsyncIterator, Dict, List, Optional

import websockets

from asynctradier.common import (
    Duration,
    EventType,
    OptionType,
    OrderClass,
    OrderSide,
    OrderType,
)
from asynctradier.common.account_balance import AccountBalance
from asynctradier.common.calendar import Calendar
from asynctradier.common.event import Event
from asynctradier.common.expiration import Expiration
from asynctradier.common.gain_loss import ProfitLoss
from asynctradier.common.option_contract import OptionContract
from asynctradier.common.order import Order
from asynctradier.common.position import Position
from asynctradier.common.quote import Quote
from asynctradier.common.user_profile import UserAccount
from asynctradier.exceptions import (
    APINotAvailable,
    InvalidDateFormat,
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
        self.sandbox = sandbox

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

    async def _get_streaming_account_session(self) -> Dict[str, str]:
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
            option_type (OptionType, optional): Filter by option type. Defaults to None.
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

    async def get_option_strikes(
        self, symbol: str, expiration_date: str
    ) -> List[float]:
        """
        Get option strikes for a symbol.

        Args:
            symbol (str): The symbol.
            expiration_date (str): The expiration date (YYYY-MM-DD).
        """
        if not is_valid_expiration_date(expiration_date):
            raise InvalidExiprationDate(expiration_date)

        url = "/v1/markets/options/strikes"
        params = {
            "symbol": symbol,
            "expiration": expiration_date,
        }
        response = await self.session.get(url, params=params)

        # if no strikes or strikes is None, return empty list
        if response.get("strikes") is None:
            return []
        return response.get("strikes", {}).get("strike", [])

    async def get_option_expirations(
        self,
        symbol: str,
        strikes: bool = False,
        contract_size: bool = False,
        expiration_type: bool = False,
    ) -> List[Expiration]:
        """
        Retrieves the option expirations for a given symbol.

        Args:
            symbol (str): The symbol for which to retrieve option expirations.
            strikes (bool, optional): Whether to include strike prices in the response. Defaults to False.
            contract_size (bool, optional): Whether to include contract sizes in the response. Defaults to False.
            expiration_type (bool, optional): Whether to include expiration types in the response. Defaults to False.

        Returns:
            List[Expiration]: A list of Expiration objects representing the option expirations.
        """

        url = "/v1/markets/options/expirations"
        params = {
            "symbol": symbol,
            "strikes": str(strikes).lower(),
            "contractSize": str(contract_size).lower(),
            "expirationType": str(expiration_type).lower(),
        }
        response = await self.session.get(url, params=params)

        results = []

        if response.get("expirations") is None:
            return results

        if strikes or contract_size or expiration_type:
            expirations = response.get("expirations", {}).get("expiration", [])

            if not isinstance(expirations, list):
                expirations = [expirations]

            for expiration in expirations:
                if expiration.get("strikes") is not None:
                    expiration["strikes"] = expiration["strikes"]["strike"]
                results.append(
                    Expiration(
                        **expiration,
                    )
                )
        else:
            expirations = response.get("expirations", {}).get("date", [])

            if not isinstance(expirations, list):
                expirations = [expirations]

            for expiration in expirations:
                results.append(
                    Expiration(
                        date=expiration,
                    )
                )

        return results

    async def option_lookup(self, symbol: str) -> List[str]:
        """
        Retrieves a list of option symbols for a given symbol.

        Args:
            symbol (str): The symbol for which to retrieve option symbols.

        Returns:
            List[str]: A list of option symbols.
        """
        url = "/v1/markets/options/lookup"
        params = {"underlying": symbol}
        response = await self.session.get(url, params=params)
        if response.get("symbols") is None:
            return []
        return response.get("symbols")[0].get("options", [])

    async def get_user_profile(self) -> List[UserAccount]:
        """
        Retrieves the user profile information.

        Returns:
            A list of UserProfile objects representing the user's profile information.
        """
        if self.sandbox:
            raise APINotAvailable(
                "please check the documentation for more details: https://documentation.tradier.com/brokerage-api/user/get-profile"
            )

        url = "/v1/user/profile"
        response = await self.session.get(url)

        if response.get("profile") is None:
            return []

        if not isinstance(response["profile"]["account"], list):
            accounts = [response["profile"]["account"]]
        else:
            accounts = response["profile"]["account"]

        res: List[UserAccount] = []
        for account in accounts:
            res.append(
                UserAccount(
                    **account,
                    id=response["profile"]["id"],
                    name=response["profile"]["name"],
                )
            )

        return res

    async def get_balance(self) -> AccountBalance:
        """
        Retrieves the account balance.

        Returns:
            AccountBalance: The account balance.
        """
        url = f"/v1/accounts/{self.account_id}/balances"
        response = await self.session.get(url)
        return AccountBalance(
            **response["balances"],
        )

    async def get_history(
        self,
        page: int = 1,
        limit: int = 25,
        event_type: Optional[EventType] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        symbol: Optional[str] = None,
        exact_match: bool = False,
    ) -> List[Event]:
        """
        Retrieves the account history.

        Args:
            page (int, optional): The page number of the history to retrieve. Defaults to 1.
            limit (int, optional): The number of events to retrieve per page. Defaults to 25.
            event_type (EventType, optional): The type of event to retrieve. Defaults to None.
            start (str, optional): The start date of the history to retrieve (YYYY-MM-DD). Defaults to None.
            end (str, optional): The end date of the history to retrieve (YYYY-MM-DD). Defaults to None.
            symbol (str, optional): The symbol of the event to retrieve. Defaults to None.
            exact_match (bool, optional): Whether to perform an exact match on the symbol. Defaults to False.

        Returns:
            List[Event]: A list of Event objects representing the account history.
        """
        if self.sandbox:
            raise APINotAvailable(
                "please check the documentation for more details: https://documentation.tradier.com/brokerage-api/accounts/get-account-balance"
            )

        if start is not None and not is_valid_expiration_date(start):
            raise InvalidDateFormat(start)

        if end is not None and not is_valid_expiration_date(end):
            raise InvalidDateFormat(end)

        if page is None or page < 1:
            page = 1

        if limit is None or limit < 1:
            limit = 25

        if exact_match is None:
            exact_match = False

        url = f"/v1/accounts/{self.account_id}/history"

        params = {
            "page": page,
            "limit": limit,
            "exactMatch": str(exact_match).lower(),
        }

        if event_type is not None:
            params["type"] = event_type.value

        if start is not None:
            params["start"] = start

        if end is not None:
            params["end"] = end

        if symbol is not None:
            params["symbol"] = symbol

        response = await self.session.get(url, params=params)

        if response.get("history") is None:
            return []

        if response["history"].get("event") is None:
            return []

        if not isinstance(response["history"]["event"], list):
            events = [response["history"]["event"]]
        else:
            events = response["history"]["event"]

        results: List[Event] = []

        for event in events:
            results.append(
                Event(
                    **event,
                )
            )

        return results

    async def get_gainloss(
        self,
        page: int = 1,
        limit: int = 25,
        start: Optional[str] = None,
        end: Optional[str] = None,
        symbol: Optional[str] = None,
        sort_by_close_date: bool = True,
        desc: bool = True,
    ) -> List[ProfitLoss]:
        """
        Retrieves the gain/loss information for closed positions within a specified date range.

        Args:
            page (int): The page number of the results to retrieve (default is 1).
            limit (int): The maximum number of results per page (default is 25).
            start (str, optional): The start date of the date range (format: "YYYY-MM-DD").
            end (str, optional): The end date of the date range (format: "YYYY-MM-DD").
            symbol (str, optional): The symbol of the positions to filter by.
            sort_by_close_date (bool): Whether to sort the results by close date (default is False).
            desc (bool): Whether to sort the results in descending order (default is True).

        Returns:
            List[ProfitLoss]: A list of ProfitLoss objects representing the gain/loss information.

        Raises:
            InvalidDateFormat: If the start or end date is not in the correct format.

        """

        if start is not None and not is_valid_expiration_date(start):
            raise InvalidDateFormat(start)

        if end is not None and not is_valid_expiration_date(end):
            raise InvalidDateFormat(end)

        if page is None or page < 1:
            page = 1

        if limit is None or limit < 1:
            limit = 25

        url = f"/v1/accounts/{self.account_id}/gainloss"

        params = {
            "page": page,
            "limit": limit,
            "sortBy": "closeDate" if sort_by_close_date else "openDate",
            "sort": "desc" if desc else "asc",
        }

        if start is not None:
            params["start"] = start

        if end is not None:
            params["end"] = end

        if symbol is not None:
            params["symbol"] = symbol

        response = await self.session.get(url, params=params)

        if response.get("gainloss") is None:
            return []

        if response["gainloss"].get("closed_position") is None:
            return []

        if not isinstance(response["gainloss"]["closed_position"], list):
            positions = [response["gainloss"]["closed_position"]]
        else:
            positions = response["gainloss"]["closed_position"]

        results: List[ProfitLoss] = []

        for position in positions:
            results.append(
                ProfitLoss(
                    **position,
                )
            )

        return results

    async def get_calendar(self, year: str, month: str) -> List[Calendar]:
        """
        Retrieves the calendar for a specific year and month.

        Args:
            year (str): The year in the format YYYY.
            month (str): The month in the format MM.

        Returns:
            List[Calendar]: A list of Calendar objects representing the calendar for the specified year and month.
        """

        if len(year) != 4:
            raise InvalidParameter("year must be in the format YYYY")
        if len(month) != 2:
            raise InvalidParameter("month must be in the format MM")

        if int(month) < 1 or int(month) > 12:
            raise InvalidParameter("month must be between 1 and 12")

        url = "/v1/markets/calendar"
        params = {"year": year, "month": month}

        response = await self.session.get(url, params=params)

        if response.get("calendar") is None:
            return []
        details = response["calendar"]["days"]["day"]

        results: List[Calendar] = []

        for detail in details:
            results.append(
                Calendar(
                    **detail,
                )
            )

        return results
