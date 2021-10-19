# Iterable Data Import

This library provides a framework for bulk importing data into Iterable. It reads data from the specified source 1 record at
a time, converts each record to an Iterable object using your provided map function, and batch imports the data.

## Getting Started

install from pypi

## Usage

At a high level, the library is used by constructing an `IterableDataImport` instance and calling `IterableDataImport.run` to initiate the import.

```python3
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
        source_file_path=pathlib.Path(__file__).parent / "data.json",
        source_file_format=FileFormat.NEWLINE_DELIMITED_JSON
    )
    
    idi.run(map_function)
```

## ImportAction

ImportActions represent actions that the library can perform on an IterableResource. User provided map functions should return a single ImportAction or a list of ImportActions.

The following ImportActions are currently supported:
- UpdateUserProfile
- TrackCustomEvent
- TrackPurchase

[See full class details](/src/iterable_data_import/import_action.py)

## IterableResource

IterableResources are the entities imported or updated in Iterable.

The following IterableResources are currently supported:

### UserProfile

| Property | Type | Description |
|----------|------|-------------|
| email    | str  | user email  |
|          |      |             |
|          |      |             |

[See full class details](/src/iterable_data_import/iterable_resource.py)

## Advanced Usage

wiring up an instance without the create factory