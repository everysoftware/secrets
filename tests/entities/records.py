from typing import Any

from faker import Faker

from schemes.record import RecordCreate, RecordUpdate

fake = Faker()


def get_record_create() -> RecordCreate:
    return RecordCreate(
        name=fake.catch_phrase(),
        username=fake.user_name(),
        password=fake.password(),
        url=fake.url(),
        comment={"text": fake.text()},
    )


TOTAL_RECORDS = fake.random_int(min=1, max=20)
TEST_RECORDS = [(i, get_record_create()) for i in range(1, TOTAL_RECORDS + 1)]

PER_PAGE = fake.random_int(min=1, max=TOTAL_RECORDS)
TOTAL_PAGES = TOTAL_RECORDS // PER_PAGE + (TOTAL_RECORDS % PER_PAGE > 0)
PAGINATION_RIGHT_SEQUENCE = sorted(TEST_RECORDS, key=lambda x: x[1].name)
PAGES = [
    (i // PER_PAGE + 1, PAGINATION_RIGHT_SEQUENCE[i : i + PER_PAGE])
    for i in range(0, TOTAL_RECORDS, PER_PAGE)
]


def get_record_update() -> RecordUpdate:
    return RecordUpdate(
        name=fake.catch_phrase(),
        username=fake.user_name(),
        password=fake.password(),
        url=fake.url(),
        comment={"text": fake.text()},
    )


TEST_RECORDS_FOR_UPDATE = [
    (i, get_record_update()) for i in range(1, TOTAL_RECORDS + 1)
]


def get_record_create_missing_attribute(attr: str) -> dict[str, Any]:
    record = RecordCreate(
        name=fake.catch_phrase(),
        username=fake.user_name(),
        password=fake.password(),
    )

    record_dict = record.model_dump()
    record_dict.pop(attr)

    return record_dict


def get_record_create_random_number(attr: str) -> dict[str, Any]:
    record = get_record_create()

    record_dict = record.model_dump()
    record_dict[attr] = fake.random_number()

    return record_dict


def get_record_create_comment_random_number() -> dict[str, Any]:
    record = get_record_create()

    record_dict = record.model_dump()
    record_dict["comment"]["text"] = fake.random_number()

    return record_dict


TEST_RECORDS_NEGATIVE = (
    get_record_create_missing_attribute("name"),
    get_record_create_missing_attribute("username"),
    get_record_create_missing_attribute("password"),
    get_record_create_random_number("name"),
    get_record_create_random_number("username"),
    get_record_create_random_number("password"),
    get_record_create_random_number("url"),
    get_record_create_comment_random_number(),
)

NOT_FOUND_RECORDS = [
    fake.random_int(min=TOTAL_RECORDS + 1, max=1_000_000)
    for _ in range(fake.random_int(min=1, max=10))
]

NOT_FOUND_RECORDS_FOR_PATCH = [
    (fake.random_int(min=TOTAL_RECORDS + 1, max=1_000_000), get_record_update())
    for _ in range(fake.random_int(min=1, max=10))
]
