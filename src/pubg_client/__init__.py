"""Pubg Client package docstring"""

# This import is needed to for registration of endpoints onto the client.api attribute
import pubg_client.endpoints as endpoints
import pubg_client.models as models

from ._client import Client, SHARDS
from .models._base import ModelEncoder
from ._api import API

__version__ = '0.1.4'

__all__ = [
    # Classes
    'Client',
    'API',

    # Helpers
    'ModelEncoder',

    # Constants
    'SHARDS',

    # modules
    'endpoints',
    'models',

]
