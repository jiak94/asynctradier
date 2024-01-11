import urllib.parse

import aiohttp

from asynctradier.exceptions import BadRequestException


class WebUtil:
    """
    A utility class for making asynchronous HTTP requests.
    """

    def __init__(self, base_url: str, token: str):
        """
        Initializes the WebUtil instance.

        Args:
            base_url (str): The base URL for the API.
            token (str): The authentication token.
        """
        self.base_url = base_url
        self.token = token

    async def make_request(
        self, url: str, method: str, params: dict = None, data: dict = None
    ):
        """
        Makes an asynchronous HTTP request.

        Args:
            url (str): The URL for the request.
            method (str): The HTTP method for the request.
            params (dict, optional): The query parameters for the request. Defaults to None.
            data (dict, optional): The request payload. Defaults to None.

        Returns:
            dict: The JSON response from the request.

        Raises:
            BadRequestException: If the request fails or returns an error.
        """
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
            }
            async with session.request(
                method, url, params=params, headers=headers, data=data
            ) as resp:
                if resp.status != 200:
                    raise BadRequestException(resp.status, await resp.text())
                response = await resp.json()

                if "errors" in response:
                    raise BadRequestException(400, response["errors"]["error"])
                return response

    async def get(self, path: str, params: dict = None):
        """
        Makes an asynchronous GET request.

        Args:
            path (str): The path for the request.
            params (dict, optional): The query parameters for the request. Defaults to None.

        Returns:
            dict: The JSON response from the request.

        Raises:
            BadRequestException: If the request fails or returns an error.
        """
        url = urllib.parse.urljoin(self.base_url, path)
        return await self.make_request(url, "GET", params=params)

    async def post(self, path: str, data: dict = None):
        """
        Makes an asynchronous POST request.

        Args:
            path (str): The path for the request.
            data (dict, optional): The request payload. Defaults to None.

        Returns:
            dict: The JSON response from the request.

        Raises:
            BadRequestException: If the request fails or returns an error.
        """
        url = urllib.parse.urljoin(self.base_url, path)
        return await self.make_request(url, "POST", data=data)

    async def delete(self, path: str):
        """
        Makes an asynchronous DELETE request.

        Args:
            path (str): The path for the request.

        Returns:
            dict: The JSON response from the request.

        Raises:
            BadRequestException: If the request fails or returns an error.
        """
        url = urllib.parse.urljoin(self.base_url, path)
        return await self.make_request(url, "DELETE")

    async def put(self, path: str, data: dict = None):
        """
        Makes an asynchronous PUT request.

        Args:
            path (str): The path for the request.
            data (dict, optional): The request payload. Defaults to None.

        Returns:
            dict: The JSON response from the request.

        Raises:
            BadRequestException: If the request fails or returns an error.
        """
        url = urllib.parse.urljoin(self.base_url, path)
        return await self.make_request(url, "PUT", data=data)
