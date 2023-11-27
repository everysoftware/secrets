import enum


class UserRole(enum.Enum):
    ADMIN = enum.auto()
    USER = enum.auto()
    GUEST = enum.auto()
