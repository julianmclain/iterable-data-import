from pytest_mock import MockerFixture
from iterable_data_import import (
    SyncApiImporter,
    UserProfile,
    UpdateUserProfile,
    TrackCustomEvent,
    CustomEvent,
    CommerceItem,
    Purchase,
    TrackPurchase,
)

user = UserProfile(email="test@iterable.com")
update_user_action = UpdateUserProfile(user)

event = CustomEvent("test event", email="test@iterable.com")
track_event_action = TrackCustomEvent(event)

commerce_item = CommerceItem("1", "shoes", 99.0, 1)
purchase = Purchase(user, [commerce_item], 99.0)
track_purchase_action = TrackPurchase(purchase)


def test_handle_update_user_adds_to_batch(mocker: MockerFixture) -> None:
    importer = SyncApiImporter("some_api_key")
    mocker.patch("os.remove")
