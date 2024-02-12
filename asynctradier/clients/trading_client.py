from typing import List, Optional

from asynctradier.common import Duration, OptionType, OrderClass, OrderSide, OrderType
from asynctradier.common.option_contract import OptionContract
from asynctradier.common.order import Order
from asynctradier.exceptions import (
    InvalidExiprationDate,
    InvalidOptionType,
    InvalidParameter,
    InvalidStrikeType,
    MissingRequiredParameter,
)
from asynctradier.utils.common import build_option_symbol, is_valid_expiration_date
from asynctradier.utils.webutils import WebUtil


class TradingClient:
    """
    A client for trading operations.

    Args:
        session (WebUtil): The session object for making HTTP requests.
        account_id (str): The account ID associated with the client.
        token (str): The authentication token for accessing the trading API.
        sandbox (bool, optional): Whether to use the sandbox environment. Defaults to False.
    """

    def __init__(
        self, session: WebUtil, account_id: str, token: str, sandbox: bool = False
    ) -> None:
        self.session = session
        self.account_id = account_id
        self.token = token
        self.sandbox = sandbox

    async def buy_stock(
        self,
        symbol: str,
        quantity: int,
        order_type: OrderType = OrderType.market,
        order_duration: Duration = Duration.day,
        tag: Optional[str] = None,
        price: Optional[float] = None,
        stop: Optional[float] = None,
    ):
        """
        Place a buy stock order.

        Args:
            symbol (str): The symbol of the stock.
            quantity (int): The quantity of the stock to buy.
            order_type (OrderType, optional): The type of the order. Defaults to OrderType.market.
            order_duration (Duration, optional): The duration of the order. Defaults to Duration.day.
            tag (str, optional): An optional tag for the order. Defaults to None.
            price (float, optional): The price at which to place the order. Required for limit orders. Defaults to None.
            stop (float, optional): The stop price for the order. Required for stop orders. Defaults to None.

        Returns:
            Order: The Order object.
        """
        return await self._stock_operation(
            OrderSide.buy,
            symbol,
            quantity,
            order_type,
            order_duration,
            tag,
            price,
            stop,
        )

    async def sell_stock(
        self,
        symbol: str,
        quantity: int,
        order_type: OrderType = OrderType.market,
        order_duration: Duration = Duration.day,
        tag: Optional[str] = None,
        price: Optional[float] = None,
        stop: Optional[float] = None,
    ):
        """
        Sell a stock with the specified parameters.

        Args:
            symbol (str): The symbol of the stock to sell.
            quantity (int): The quantity of shares to sell.
            order_type (OrderType, optional): The type of order to place. Defaults to OrderType.market.
            order_duration (Duration, optional): The duration of the order. Defaults to Duration.day.
            tag (str, optional): An optional tag for the order. Defaults to None.
            price (float, optional): The price at which to sell the stock. Defaults to None.
            stop (float, optional): The stop price for a stop order. Defaults to None.

        Returns:
            The result of the stock operation.
        """
        return await self._stock_operation(
            OrderSide.sell,
            symbol,
            quantity,
            order_type,
            order_duration,
            tag,
            price,
            stop,
        )

    async def _stock_operation(
        self,
        side: OrderSide,
        symbol: str,
        quantity: int,
        order_type: OrderType = OrderType.market,
        order_duration: Duration = Duration.day,
        tag: Optional[str] = None,
        price: Optional[float] = None,
        stop: Optional[float] = None,
    ):
        """
        Executes a stock operation, such as buying or selling a stock.

        Args:
            side (OrderSide): The side of the order, either 'buy' or 'sell'.
            symbol (str): The symbol of the stock.
            quantity (int): The quantity of the stock to buy or sell.
            order_type (OrderType, optional): The type of the order. Defaults to OrderType.market.
            order_duration (Duration, optional): The duration of the order. Defaults to Duration.day.
            tag (str, optional): An optional tag for the order. Defaults to None.
            price (float, optional): The price at which to execute the order. Required for limit orders. Defaults to None.
            stop (float, optional): The stop price for stop orders. Required for stop orders. Defaults to None.

        Raises:
            MissingRequiredParameter: If price is not specified for limit orders or stop is not specified for stop orders.

        Returns:
            Order: The executed order.
        """

        if order_type == OrderType.limit and price is None:
            raise MissingRequiredParameter("Price must be specified for limit orders")

        if order_type == OrderType.stop and stop is None:
            raise MissingRequiredParameter("Stop must be specified for stop orders")

        url = f"/v1/accounts/{self.account_id}/orders"

        params = {
            "class": OrderClass.equity.value,
            "symbol": symbol,
            "side": side.value,
            "quantity": str(quantity),
            "type": order_type.value,
            "duration": order_duration.value,
            "price": str(price) if price is not None else "",
            "stop": str(stop) if stop is not None else "",
            "tag": tag,
        }

        response = await self.session.post(url, data=params)
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
