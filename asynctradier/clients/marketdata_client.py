from typing import List, Optional

from asynctradier.common import OptionType
from asynctradier.common.calendar import Calendar
from asynctradier.common.expiration import Expiration
from asynctradier.common.quote import Quote
from asynctradier.exceptions import InvalidExiprationDate, InvalidParameter
from asynctradier.utils.common import is_valid_expiration_date
from asynctradier.utils.webutils import WebUtil


class MarketDataClient:
    """
    A client for accessing market data.

    Args:
        session (WebUtil): The session object used for making HTTP requests.
        account_id (str): The account ID associated with the client.
        token (str): The authentication token for accessing the market data.
        sandbox (bool, optional): Whether to use the sandbox environment. Defaults to False.
    """

    def __init__(
        self, session: WebUtil, account_id: str, token: str, sandbox: bool = False
    ) -> None:
        self.session = session
        self.account_id = account_id
        self.token = token
        self.sandbox = sandbox

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
