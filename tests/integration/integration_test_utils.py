import logging
import time
import json
import random
from pathlib import PurePath
from typing import Dict, Any
from iterablepythonwrapper.client import IterableApi
from faker import Faker


logger = logging.getLogger("utils")
fake = Faker()
TIMEOUT_SECONDS = 10


class IterableApiHelpers:
    def __init__(self, api_key: str) -> None:
        self.api_client = IterableApi(api_key)

    def get_user(self, email: str, retries: int = 10) -> Dict[str, Any]:
        if retries <= 0:
            raise Exception(f"Unable to get user: {email}")
        else:
            response = self.api_client.get_user_by_email(email)
            if "user" not in response["body"]:
                logger.debug(
                    f"Failed to get user, retrying in {TIMEOUT_SECONDS} seconds"
                )
                time.sleep(TIMEOUT_SECONDS)
                return self.get_user(email, retries - 1)
            else:
                return response["body"]["user"]


def generate_csv_file(path: PurePath, num_records: int) -> None:
    with open(path, "w") as f:
        f.write("id,email,lifetime_value,street_address,city,state,zip,loves_pizza\n")
        for i in range(0, num_records):
            user_id = random.randint(1, 100000000000)
            email = fake.first_name() + str(user_id) + "@placeholder.email"
            ltv = random.randint(1, 100)
            f.write(
                f"{user_id},{email},{ltv},71 Stevenson St.,San Francisco,CA,94103,true\n"
            )


def generate_newline_delimited_json_file(path: PurePath, num_records: int) -> None:
    with open(path, "w") as f:
        for i in range(1, num_records + 1):
            user_id = random.randint(1, 100000000000)
            email = fake.first_name() + str(user_id) + "@placeholder.email"
            ltv = random.randint(1, 100)
            record = {
                "id": user_id,
                "email": email,
                "lifetime_value": ltv,
                "address": {
                    "street_address": "71 Stevenson St.",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "941043",
                },
                "loves_pizza": True,
            }
            f.write(json.dumps(record) + "\n")


def random_email() -> str:
    email = fake.user_name() + str(random.randint(0, 1000000)) + "@placeholder.email"
    return email


def random_user_id() -> str:
    user_id = fake.user_name() + str(random.randint(0, 1000000))
    return user_id
