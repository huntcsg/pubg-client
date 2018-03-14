"""The pubg_client package is somewhat nested, in terms of files to ease concurrent development across many developers.
However, the intention is that the usage of this package is mostly done from the `pubg_client` module, and the `models`
and `endpoints` modules.

From this top level module, the following classes are available:

**Main Classes**

    - :class:`~pubg_client._client.Client`
    - :class:`~pubg_client._api.API`

**Constants**

    - :const:`~pubg_client._client.SHARDS`

**Helpers**

    - :class:`~pubg_client.models._base.ModelEncoder`

**Namespaces**

    - :mod:`~pubg_client.models`
    - :mod:`~pubg_client.endpoints`
"""

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
