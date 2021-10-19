# Iterable Data Import

This library provides a framework for bulk importing data into Iterable. 

## Getting Started

install from pypi

## Usage

To run an import, create an`IterableDataImport` instance and call `IterableDataImport.run` with a function that accepts 
a `SourceDataRecord` and returns an [ImportAction](#ImportAction). `SourceDataRecord` is a type alias for `Dict[str, Any]`. When `IterableDataImort.run` is called, the library will:
1. Stream records 1 at a time from your data source
2. Parse each record into a `SourceDataRecord`
3. Call your function to map the `SourceDataRecord` to an Iterable `ImportAction`
4. Use batching to efficiently transfer the data to Iterable (only via API for now)

Given the following example data:
```
id,email,lifetime_value
1,test@iterable.com,79
```

Example usage:
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
        source_file_path=pathlib.Path(__file__).parent / "data.csv",
        source_file_format=FileFormat.CSV
    )
    
    idi.run(map_function)
```

## ImportAction

ImportActions represent actions that the library can perform on an IterableResource. User provided map functions should return a single ImportAction or a list of ImportActions.

[See full class details](/src/iterable_data_import/import_action.py)

### UpdateUserProfile

| Property     | Type        | Description                | Notes |
|--------------|-------------|----------------------------|-------|
| user         | UserProfile | The user to update         |       |

### TrackCustomEvent

| Property     | Type        | Description                | Notes |
|--------------|-------------|----------------------------|-------|
| custom_event | CustomEvent | The custom event to create |       |

### TrackPurchase

| Property     | Type        | Description                | Notes |
|--------------|-------------|----------------------------|-------|
| purchase     | Purchase    | The purchase to create     |       |


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

### CustomEvent

### CommerceItem

### Purchase