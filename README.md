# Iterable Data Import

`iterable-data-import` is a library for ad-hoc bulk imports to [Iterable](https://iterable.com). 

## Getting Started

install from pypi

## Usage

To run an import, create an`IterableDataImport` instance and call
`IterableDataImport.run` with a function that accepts a
[SourceDataRecord](#SourceDataRecord) and returns an
[ImportAction](#ImportAction). When `IterableDataImort.run` is called, the
library will:
1. Stream records 1 at a time from your data source
2. Parse each record into a `SourceDataRecord`
3. Call your function to map the `SourceDataRecord` to an Iterable
   `ImportAction`
4. Use batching to efficiently transfer the data to Iterable

Given the following example data:
```
id,email,lifetime_value
1,test@iterable.com,79
```

Example usage:
```python
import pathlib

from iterable_data_import import (
    IterableDataImport,
    FileFormat,
    UserProfile,
    ImportAction,
    UpdateUserProfile,
    SourceDataRecord,
)

if __name__ == "__main__":
    def map_function(record: SourceDataRecord) -> ImportAction:
        email = record["email"]
        user_id = record["id"]
        data_fields = {"ltv": record["lifetime_value"]}
        user = UserProfile(email, user_id, data_fields)
        return UpdateUserProfile(user)

    idi = IterableDataImport.create(
        api_key="some_api_key",
        source_file_path=pathlib.Path(__file__).parent / "data.csv",
        source_file_format=FileFormat.CSV
    )
    
    idi.run(map_function)
```

## SourceDataRecord

When you run the import, each source record will be deserialized to a
`SourceDataRecord`, which is a type alias for `Dict[str, object]`.

### Newline Delimited JSON data

If you select `FileFormat.NEWLINE_DELIMITED_JSON` as your source file format,
the `SourceDataRecord` passed into your map function will be a `Dict[str, object]`
where the `object` type is one of the Python types that can be decoded from JSON.

`iterable-data-import` uses the `json` standard library module to decode your
source JSON objects. For documentation on how `json` translates JSON values to
Python types, see the standard library page for [json - JSON encoder and
decoder](https://docs.python.org/3/library/json.html?highlight=json%20loads#encoders-and-decoders).

### CSV data

If you select `FileFormat.CSV` as your source file format, the
`SourceDataRecord` passed into your map function will be a `Dict[str, str]`. You
may need to cast the values in the `dict` from `str` to their proper Python
type. 

`iterable-data-import` uses a `DictReader` from the `csv` standard library
module to decode your source CSV rows. For additional documentation on how the
`DictReader` parses each csv row, see the standard library page for [csv - CSV
File Reading and
Writing](https://docs.python.org/3/library/csv.html?highlight=csv#csv.DictReader).


## ImportAction

`ImportAction` represents actions that the library can perform on an
[IterableResource](#IterableResource). Your map function should return a single
`ImportAction` or a list of `ImportAction`.

[See full class details](/src/iterable_data_import/import_action.py)

### UpdateUserProfile

```python
class UpdateUserProfile(ImportAction):
    def __init__(self, user: UserProfile) -> None:
```

### TrackCustomEvent

```python
class TrackCustomEvent(ImportAction):
    def __init__(self, event: CustomEvent) -> None:
```

### TrackPurchase

```python
class TrackPurchase(ImportAction):
    def __init__(self, purchase: Purchase) -> None:
```

## IterableResource

`IterableResource` represents the entities to be imported or updated in
Iterable.

[See full class details](/src/iterable_data_import/iterable_resource.py)

### UserProfile

At least 1 of `email` or `user_id` must be provided.
```python3
class UserProfile(IterableResource):
    def __init__(
        self,
        email: Optional[str] = None,
        user_id: Optional[str] = None,
        data_fields: Optional[Dict[str, Any]] = None,
        prefer_user_id: bool = False,
        merge_nested_objects: bool = False,
    ) -> None:
```

### CustomEvent

At least 1 of `email` or `user_id` must be provided. `created_at` is a Unix Epoch.
```python
class CustomEvent(IterableResource):
    def __init__(
        self,
        event_name: str,
        email: Optional[str] = None,
        user_id: Optional[str] = None,
        data_fields: Optional[Dict[str, Any]] = None,
        event_id: Optional[str] = None,
        template_id: Optional[int] = None,
        campaign_id: Optional[int] = None,
        created_at: Optional[int] = None,
    ):
```

### CommerceItem

```python
class CommerceItem(IterableResource):
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
        data_fields: Optional[Dict[str, Any]] = None,
    ) -> None:
```

### Purchase

`created_at` is a Unix Epoch.
```python
class Purchase(IterableResource):
    def __init__(
        self,
        user: UserProfile,
        items: List[CommerceItem],
        total: float,
        created_at: Optional[int] = None,
        data_fields: Optional[Dict[str, Any]] = None,
        purchase_id: Optional[str] = None,
        campaign_id: Optional[int] = None,
        template_id: Optional[int] = None,
    ):
```
