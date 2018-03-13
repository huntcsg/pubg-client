from .._api import API
from ..models.status import Status
from ._base import Endpoint


@API.register('status', Status())
class Status(Endpoint):
    """The status endpoint"""
    method = 'GET'
    """The Method"""

    path = 'status'
    """The path"""
