from typing import Optional, Dict, List


class IterableResource:
    """
    Representation of Iterable resources
    """

    @staticmethod
    def _remove_none_values(api_obj: Dict[str, object]) -> Dict[str, object]:
        return {k: v for k, v in api_obj.items() if v is not None}


class CustomEvent(IterableResource):
    """
    An Iterable custom event
    """

    def __init__(
        self,
        event_name: str,
        email: Optional[str] = None,
        user_id: Optional[str] = None,
        data_fields: Optional[Dict[str, object]] = None,
        event_id: Optional[str] = None,
        template_id: Optional[int] = None,
        campaign_id: Optional[int] = None,
        created_at: Optional[int] = None,
    ):
        if not event_name:
            raise ValueError("Custom events must have an event_name")

        if not email and not user_id:
            raise ValueError("Custom events must have an email or user_id")

        if data_fields is None:
            data_fields = {}

        self.event_name = event_name
        self.email = email
        self.user_id = user_id
        self.data_fields = data_fields
        self.event_id = event_id
        self.template_id = template_id
        self.campaign_id = campaign_id
        self.created_at = created_at

    @property
    def to_api_dict(self):
        event_dict = {
            "eventName": self.event_name,
            "email": self.email,
            "userId": self.user_id,
            "dataFields": self.data_fields,
            "id": self.event_id,
            "templateId": self.template_id,
            "campaignId": self.campaign_id,
            "createdAt": self.created_at,
        }
        return self._remove_none_values(event_dict)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.event_name}, {self.email}, {self.user_id})"


class UserProfile(IterableResource):
    """
    An Iterable user profile
    """

    def __init__(
        self,
        email: Optional[str] = None,
        user_id: Optional[str] = None,
        data_fields: Optional[Dict[str, object]] = None,
        prefer_user_id: bool = False,
        merge_nested_objects: bool = False,
    ) -> None:
        if data_fields is None:
            data_fields = {}

        if not email and not user_id:
            raise ValueError("User profiles must have an email or user_id")

        self.email = email
        self.user_id = user_id
        self.data_fields = data_fields
        self.prefer_user_id = prefer_user_id
        self.merge_nested_objects = merge_nested_objects

    @property
    def to_api_dict(self):
        user_dict = {
            "email": self.email,
            "userId": self.user_id,
            "dataFields": self.data_fields,
            "preferUserId": self.prefer_user_id,
            "mergeNestedObjects": self.merge_nested_objects,
        }
        return user_dict

    def __repr__(self):
        identifiers = [x for x in [self.email, self.user_id] if x]
        return f'{self.__class__.__name__}({", ".join(identifiers)})'


class CommerceItem(IterableResource):
    """
    An Iterable commerce item
    """

    def __init__(
        self,
        item_id: str,
        name: str,
        price: float,
        quantity: int,
        sku: Optional[str] = None,
        description: Optional[str] = None,
        categories: Optional[List[str]] = None,
        image_url: Optional[str] = None,
        url: Optional[str] = None,
        data_fields: Optional[Dict[str, object]] = None,
    ) -> None:
        if not item_id or not name or not price or not quantity:
            raise ValueError(
                "Commerce items must contain an item_id, name, price, and quantity"
            )

        self.item_id = item_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.sku = sku
        self.description = description
        self.categories = categories
        self.image_url = image_url
        self.url = url
        self.data_fields = data_fields

    @property
    def to_api_dict(self):
        commerce_item_dict = {
            "id": self.item_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "sku": self.sku,
            "description": self.description,
            "categories": self.categories,
            "imageUrl": self.image_url,
            "url": self.url,
            "dataFields": self.data_fields,
        }
        return self._remove_none_values(commerce_item_dict)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.item_id}, {self.name}, {self.price}, {self.quantity})"


class Purchase(IterableResource):
    """
    An Iterable purchase
    """

    def __init__(
        self,
        user: UserProfile,
        items: List[CommerceItem],
        total: float,
        created_at: Optional[int] = None,
        data_fields: Optional[Dict[str, object]] = None,
        purchase_id: Optional[str] = None,
        campaign_id: Optional[int] = None,
        template_id: Optional[int] = None,
    ):
        if not user or not items or not total:
            raise ValueError("Purchases must contain a user, items, and total")

        self.user = user
        self.items = items
        self.total = total
        self.created_at = created_at
        self.data_fields = data_fields
        self.purchase_id = purchase_id
        self.campaign_id = campaign_id
        self.template_id = template_id

    @property
    def to_api_dict(self):
        purchase_dict = {
            "id": self.purchase_id,
            "user": self.user.to_api_dict,
            "items": [item.to_api_dict for item in self.items],
            "campaignId": self.campaign_id,
            "templateId": self.template_id,
            "total": self.total,
            "createdAt": self.created_at,
            "dataFields": self.data_fields,
        }
        return self._remove_none_values(purchase_dict)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.user}, [{", ".join([str(item) for item in self.items])}], {self.total})'
