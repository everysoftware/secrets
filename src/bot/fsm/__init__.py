from .auth import RegisterGroup, LoginGroup
from .main import MainGroup
from .record import RecordGroup, UpdateRecordGroup, AddRecordGroup
from .service import ConfirmationGroup
from .user import ProfileMasterEditingGroup, ProfileGroup, ProfilePasswordEditingGroup

__all__ = (
    'RegisterGroup',
    'LoginGroup',
    'MainGroup',
    'RecordGroup',
    'UpdateRecordGroup',
    'AddRecordGroup',
    'ProfileGroup',
    'ProfilePasswordEditingGroup',
    'ProfileMasterEditingGroup',
    'ConfirmationGroup'
)
