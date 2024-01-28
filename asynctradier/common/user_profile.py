from asynctradier.common import AccountStatus, AccountType, Classification


class UserAccount:
    """
    Represents a user profile with various attributes.

    Attributes:
        id (str): The ID of the user profile.
        name (str): The name of the user profile.
        account_number (str): The account number associated with the user profile.
        classification (Classification): The classification of the user profile.
        date_created (str): The date when the user profile was created.
        day_trader (bool): Indicates whether the user is a day trader or not.
        option_level (int): The option level of the user profile.
        status (AccountStatus): The status of the user profile.
        type (AccountType): The type of the user profile.
        last_update_date (str): The date of the last update to the user profile.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.account_number = kwargs.get("account_number")
        self.classification = Classification(kwargs.get("classification"))
        self.date_created = kwargs.get("date_created")
        self.day_trader = kwargs.get("day_trader")
        self.option_level = (
            int(kwargs.get("option_level")) if kwargs.get("option_level") else None
        )
        self.status = (
            AccountStatus(kwargs.get("status")) if kwargs.get("status") else None
        )
        self.type = AccountType(kwargs.get("type")) if kwargs.get("type") else None
        self.last_update_date = kwargs.get("last_update_date")

    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name,
            "account_number": self.account_number,
            "classification": (
                self.classification.value if self.classification else None
            ),
            "date_created": self.date_created,
            "day_trader": self.day_trader,
            "option_level": self.option_level,
            "status": self.status.value if self.status else None,
            "type": self.type.value if self.type else None,
            "last_update_date": self.last_update_date,
        }
