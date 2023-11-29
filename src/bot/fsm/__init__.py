from .auth import RegisterGroup, LoginGroup
from .main import MainGroup
from .record import RecordGroup, EditRecordGroup, AddRecordGroup
from .service import VerificationGroup
from .user import ProfileMasterEditingGroup, ProfileGroup, ProfilePasswordEditingGroup

__all__ = (
    'RegisterGroup',
    'LoginGroup',
    'MainGroup',
    'RecordGroup',
    'EditRecordGroup',
    'AddRecordGroup',
    'ProfileGroup',
    'ProfilePasswordEditingGroup',
    'ProfileMasterEditingGroup',
    'VerificationGroup'
)
