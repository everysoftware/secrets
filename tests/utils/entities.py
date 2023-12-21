from api.records.schemes import RecordCreate, RecordUpdate
from app.api.auth.schemes import UserCreate, TwoFALogin

TEST_USER_CREATE = UserCreate(
    email="test@test.com",
    password="1234",
    master_password="4321",
    first_name="Ivan"
)

TEST_USER_LOGIN = {
    "username": TEST_USER_CREATE.email,
    "password": TEST_USER_CREATE.password
}

TEST_USER_2FA = TwoFALogin(
    master_password=TEST_USER_CREATE.master_password
)

TEST_RECORD_CREATE = RecordCreate(
    name="Test Record",
    username="Test Username",
    password="Test Password",
    url="https://testurl.com",
    comment={"text": "Test Comment"}
)

TEST_RECORD_UPDATE = RecordUpdate(
    name="Test Record Update",
    username="Test Username Update",
    password="Test Password Update",
    url="https://testurlupdate.com",
    comment={"text": "Test Comment Update"}
)
