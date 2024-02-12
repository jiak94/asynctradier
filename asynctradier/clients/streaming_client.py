import json
from typing import AsyncIterator, Dict, List

import websockets

from asynctradier.common import MarketDataType
from asynctradier.common.market_data import MarketData
from asynctradier.common.order import Order
from asynctradier.utils.webutils import WebUtil


class StreamingClient:
    """
    A client for streaming market data and order events.

    Args:
        session (WebUtil): The session object for making HTTP requests.
        account_id (str): The ID of the account.
        token (str): The authentication token.
        sandbox (bool, optional): Whether to use the sandbox environment. Defaults to False.
    """

    def __init__(
        self, session: WebUtil, account_id: str, token: str, sandbox: bool = False
    ) -> None:
        self.session = session
        self.account_id = account_id
        self.token = token
        self.sandbox = sandbox

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

    async def _get_streaming_account_session(self) -> Dict[str, str]:
        """
        Get the streaming account session.

        Returns:
            str: The streaming account session.
        """
        url = "/v1/accounts/events/session"
        response = await self.session.post(url)
        return response

    async def _get_streaming_market_data_session(self) -> Dict[str, str]:
        """
        Get the streaming quote session.

        Returns:
            str: The streaming quote session.
        """
        url = "/v1/markets/events/session"
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
                        yield Order(**response)

    async def stream_market_data(
        self,
        symbols: List[str],
        filters: List[MarketDataType] = None,
        linebreak: bool = True,
        valid_only: bool = True,
        advanced_details: bool = True,
    ) -> AsyncIterator[MarketData]:
        """
        Streams market data for the given symbols.

        Args:
            symbols (List[str]): The list of symbols to stream market data for.
            filters (List[MarketDataType], optional): The list of market data types to filter. Defaults to None.
            linebreak (bool, optional): Whether to include linebreaks in the streamed data. Defaults to True.
            valid_only (bool, optional): Whether to include only valid market data. Defaults to True.
            advanced_details (bool, optional): Whether to include advanced details in the market data. Defaults to True.

        Yields:
            MarketData: The streamed market data.

        """

        streaming_session = await self._get_streaming_market_data_session()
        uri = "wss://ws.tradier.com/v1/markets/events"
        session_id = streaming_session["stream"]["sessionid"]

        if filters is None:
            filters = []
        filters.append(MarketDataType.trade)

        async with websockets.connect(uri, ssl=True, compression=None) as websocket:
            payload = {
                "symbols": symbols,
                "sessionid": session_id,
                "linebreak": linebreak,
                "filter": filters,
                "validOnly": valid_only,
                "advancedDetails": advanced_details,
            }
            payload = json.dumps(payload)

            await websocket.send(payload)

            while True:
                response = json.loads(await websocket.recv())
                yield MarketData(**response)
