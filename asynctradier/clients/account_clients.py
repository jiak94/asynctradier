from typing import List, Optional

from asynctradier.common import EventType
from asynctradier.common.account_balance import AccountBalance
from asynctradier.common.event import Event
from asynctradier.common.gain_loss import ProfitLoss
from asynctradier.common.order import Order
from asynctradier.common.position import Position
from asynctradier.common.user_profile import UserAccount
from asynctradier.exceptions import APINotAvailable, InvalidDateFormat
from asynctradier.utils.common import is_valid_expiration_date
from asynctradier.utils.webutils import WebUtil


class AccountClient:
    """
    A client for interacting with the Tradier Account API.

    Args:
        session (WebUtil): The session object used for making HTTP requests.
        account_id (str): The account ID.
        token (str): The API token.
        sandbox (bool, optional): Whether to use the sandbox environment. Defaults to False.
    """

    def __init__(
        self, session: WebUtil, account_id: str, token: str, sandbox: bool = False
    ) -> None:
        self.session = session
        self.account_id = account_id
        self.token = token
        self.sandbox = sandbox

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
