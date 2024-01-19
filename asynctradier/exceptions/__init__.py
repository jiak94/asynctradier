class InvalidExiprationDate(Exception):
    """
    Exception raised when the expiration date is not valid.

    Attributes:
        expiration (str): The invalid expiration date.
    """

    def __init__(self, expiration: str):
        self.expiration = expiration
        super().__init__(
            f"ExpirationDate {expiration} is not valid. Valid values is: YYYY-MM-DD"
        )


class InvalidStrikeType(Exception):
    """
    Exception raised when the strike type is not valid.

    Attributes:
        strike (any): The invalid strike type.
    """

    def __init__(self, strike: any):
        self.strike = strike
        super().__init__(
            f"Strike type {type(strike)} is not valid. Valid values are: float, int"
        )


class MissingRequiredParameter(Exception):
    """
    Exception raised when a required parameter is missing.

    Attributes:
        msg (str): The error message.
    """

    def __init__(self, msg: str):
        super().__init__(msg)


class InvalidOptionType(Exception):
    """
    Exception raised when the option type is not valid.

    Attributes:
        option_type (str): The invalid option type.
    """

    def __init__(self, option_type: str) -> None:
        super().__init__(
            f"Option type {option_type} is not valid. Valid values are: CALL, PUT"
        )


class InvalidParameter(Exception):
    """
    Exception raised when a parameter is not valid.

    Attributes:
        msg (str): The error message.
    """

    def __init__(self, msg: str) -> None:
        super().__init__(f"Parameter is not valid. {msg}")


class BadRequestException(Exception):
    """
    Exception raised when a bad request is made.

    Attributes:
        code (int): The HTTP status code of the bad request.
        msg (str): The error message.
    """

    def __init__(self, code: int, msg: str) -> None:
        super().__init__(f"Request failed: {code}, msg: {msg}")


class APINotAvailable(Exception):
    """
    Exception raised when the API is not available.

    Attributes:
        msg (str): The error message.
    """

    def __init__(self, msg: str) -> None:
        super().__init__(f"API is not available. {msg}")


class InvalidDateFormat(Exception):
    """
    Exception raised when the date format is not valid.

    Attributes:
        date (str): The invalid date.
    """

    def __init__(self, date: str) -> None:
        super().__init__(
            f"Date format {date} is not valid. Valid values is: YYYY-MM-DD"
        )
