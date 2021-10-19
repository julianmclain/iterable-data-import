from iterable_data_import.iterable_resource import UserProfile, CustomEvent, Purchase


class ImportAction:
    """
    An action that can be performed by an Iterable import service
    """

    pass


class UpdateUserProfile(ImportAction):
    """
    An instruction to update a user profile
    """

    def __init__(self, user: UserProfile) -> None:
        self.user = user


class TrackCustomEvent(ImportAction):
    """
    An instruction to track a custom event
    """

    def __init__(self, event: CustomEvent) -> None:
        self.event = event


class TrackPurchase(ImportAction):
    """
    An instruction to track a purchase
    """

    def __init__(self, purchase: Purchase) -> None:
        self.purchase = purchase
