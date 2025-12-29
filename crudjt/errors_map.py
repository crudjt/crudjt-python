from .errors import InternalError
from .errors import InvalidState

ERRORS = {
    'XX000': InternalError,
    '55JT01': InvalidState
}
