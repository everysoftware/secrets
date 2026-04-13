from .auth import LoginGroup, RegisterGroup
from .main import MainGroup
from .record import AddRecordGroup, EditRecordGroup, RecordGroup
from .service import VerificationGroup
from .user import (ProfileGroup, ProfileMasterEditingGroup,
                   ProfilePasswordEditingGroup)

__all__ = (
    "RegisterGroup",
    "LoginGroup",
    "MainGroup",
    "RecordGroup",
    "EditRecordGroup",
    "AddRecordGroup",
    "ProfileGroup",
    "ProfilePasswordEditingGroup",
    "ProfileMasterEditingGroup",
    "VerificationGroup",
)
