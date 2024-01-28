from asynctradier.common import MarketStatus


class Calendar:
    """
    Represents a calendar object that contains information about market status and trading hours for a specific date.
    """

    def __init__(self, **kwargs):
        self.date = kwargs.get("date")
        self.status = (
            MarketStatus(kwargs.get("status")) if kwargs.get("status") else None
        )
        self.description = kwargs.get("description")
        self.premarket_start = kwargs.get("premarket", {}).get("start")
        self.premarket_end = kwargs.get("premarket", {}).get("end")
        self.regular_start = kwargs.get("open", {}).get("start")
        self.regular_end = kwargs.get("open", {}).get("end")
        self.postmarket_start = kwargs.get("postmarket", {}).get("start")
        self.postmarket_end = kwargs.get("postmarket", {}).get("end")

    def to_dict(self):
        """
        Converts the Calendar object to a dictionary.

        Returns:
            dict: A dictionary representation of the Calendar object.
        """
        return {
            "date": self.date,
            "status": self.status.value,
            "description": self.description,
            "premarket": {"start": self.premarket_start, "end": self.premarket_end},
            "open": {"start": self.regular_start, "end": self.regular_end},
            "postmarket": {"start": self.postmarket_start, "end": self.postmarket_end},
        }

    def __str__(self):
        return f"Calendar(date={self.date}, status={self.status}, description={self.description}, premarket_start={self.premarket_start}, premarket_end={self.premarket_end}, regular_start={self.regular_start}, regular_end={self.regular_end}, postmarket_start={self.postmarket_start}, postmarket_end={self.postmarket_end})"
