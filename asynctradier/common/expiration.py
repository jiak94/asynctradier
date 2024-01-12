class Expiration:
    """
    Represents an expiration date for a contract.

    Attributes:
        date (str): The expiration date.
        contract_size (int): The size of the contract.
        expiration_type (str): The type of expiration.
        strikes (list): A list of strike prices.
    """

    def __init__(self, **kwargs):
        self.date = kwargs.get("date")
        self.contract_size = kwargs.get("contract_size")
        self.expiration_type = kwargs.get("expiration_type")
        self.strikes = kwargs.get("strikes")
