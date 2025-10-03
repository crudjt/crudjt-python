from .errors import InternalError
from .errors import DonateException

ERRORS = {
    'XX000': InternalError,
    'DE000': DonateException
}
