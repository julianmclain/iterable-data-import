from abc import ABCMeta
from typing import Any, Dict, List

from iterable_data_import import UserProfile, CustomEvent, Purchase


class IterableRequest(metaclass=ABCMeta):
    """
    Class representing an Iterable API request body
    """

    @property
    def to_api_dict(self) -> Dict[str, Any]:
        return {}


class BulkUserUpdateRequest(IterableRequest):
    """
    Class representing an Iterable bulk user update request body

    See: https://api.iterable.com/api/docs#users_bulkUpdateUser
    """

    def __init__(self, users: List[UserProfile]):
        self.users = users

    @property
    def to_api_dict(self) -> Dict[str, Any]:
        """
        Get the bulk update request as a dictionary structured for the Iterable API

        :return: the api request body dictionary
        """
        req_api_dict = {"users": [user.to_api_dict for user in self.users]}
        return req_api_dict


class BulkTrackCustomEventRequest(IterableRequest):
    """
    Class representing an Iterable bulk track custom event request body

    See: https://api.iterable.com/api/docs#events_trackBulk
    """

    def __init__(self, events: List[CustomEvent]):
        self.events = events

    @property
    def to_api_dict(self) -> Dict[str, Any]:
        """
        Get the bulk track custom event request as a dictionary structured for the Iterable API

        :return: the api request body dictionary
        """
        req_api_dict = {"events": [event.to_api_dict for event in self.events]}
        return req_api_dict


class TrackPurchaseRequest(IterableRequest):
    """
    Class representing an Iterable track purchase request body

    See: https://api.iterable.com/api/docs#commerce_trackPurchase
    """

    def __init__(self, purchase: Purchase):
        self.purchase = purchase

    @property
    def to_api_dict(self) -> Dict[str, Any]:
        """
        Get the track purchase request as a dictionary structured for the Iterable API

        :return: the api request body dictionary
        """
        return self.purchase.to_api_dict
