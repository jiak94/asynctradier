from asynctradier.clients.account_clients import AccountClient
from asynctradier.clients.marketdata_client import MarketDataClient
from asynctradier.clients.streaming_client import StreamingClient
from asynctradier.clients.trading_client import TradingClient
from asynctradier.utils.webutils import WebUtil


class TradierClient(AccountClient, TradingClient, MarketDataClient, StreamingClient):
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

        super().__init__(self.session, self.account_id, self.token, self.sandbox)
