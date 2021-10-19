# Iterable Data Import

This library provides a framework for bulk importing data into Iterable. 

## Getting Started

install from pypi

## Usage

To run an import, create an`IterableDataImport` instance and call
`IterableDataImport.run` with a function that accepts a `SourceDataRecord` and
returns an [ImportAction](#ImportAction). `SourceDataRecord` is a type alias for
`Dict[str, Any]`. When `IterableDataImort.run` is called, the library will:
1. Stream records 1 at a time from your data source
2. Parse each record into a `SourceDataRecord`
3. Call your function to map the `SourceDataRecord` to an Iterable
   `ImportAction`
4. Use batching to efficiently transfer the data to Iterable (only via API for
   now)

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

## ImportAction

`ImportAction` represents actions that the library can perform on an
`IterableResource`. Your map function can return a single
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

`IterableResource` represents the entities to be imported or updated in Iterable.

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

### CommerceItem

### Purchase