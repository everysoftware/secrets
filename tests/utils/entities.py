from app.api.auth.schemes import UserCreate

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

TEST_USER_2FA = {
    "master_password": TEST_USER_CREATE.master_password
}
