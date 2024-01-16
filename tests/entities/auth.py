from faker import Faker

from schemes.user import UserCreate, TwoFALogin

fake = Faker()


def get_user_create():
    return UserCreate(
        email=fake.email(),
        password=fake.password(
            length=8,
            special_chars=True,
            digits=True,
            upper_case=False,
            lower_case=False,
        ),
        master_password=fake.password(
            length=8,
            special_chars=True,
            digits=True,
            upper_case=False,
            lower_case=False,
        ),
        first_name=fake.first_name(),
    )


def get_login_data(user: UserCreate):
    return {"username": user.email, "password": user.password}


def get_2fa_data(user: UserCreate):
    return TwoFALogin(master_password=user.master_password)
