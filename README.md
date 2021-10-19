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

[See full class details](/src/iterable_data_import/import_action.py)

### UpdateUserProfile

| Property | Type        | Description        | Notes |
|----------|-------------|--------------------|-------|
| user     | UserProfile | The user to update |       |

### TrackCustomEvent

| Property     | Type        | Description                | Notes |
|--------------|-------------|----------------------------|-------|
| custom_event | CustomEvent | The custom event to create |       |

### TrackPurchase

| Property | Type     | Description            | Notes |
|----------|----------|------------------------|-------|
| purchase | Purchase | The purchase to create |       |


## IterableResource

IterableResources are the entities imported or updated in Iterable.

[See full class details](/src/iterable_data_import/iterable_resource.py)

### UserProfile

| Property             | Type                     | Description                                    | Notes                                            |
|----------------------|--------------------------|------------------------------------------------|--------------------------------------------------|
| email                | Optional[str]            | Email address                                  | Either email or user_id required; must be unique |
| user_id              | Optional[str]            | User identifier                                | Must be unique                                   |
| data_fields          | Optional[Dict[str, Any]] | Custom attributes                              |                                                  |
| prefer_user_id       | bool                     | Create a new user with user_id if nonexistent  | Default False                                    |