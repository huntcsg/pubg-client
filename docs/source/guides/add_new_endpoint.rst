Adding a New Endpoint
---------------------

1. Find or create a new python module under `src/pubg_client/endpoints/`
2. You need to know the path, method, and deserialization factory to use.

    .. code-block:: python

        from .._api import API
        from ..models import SomeFactory
        from ._base import Endpoint


        @API.register('some_unique_method_name', SomeFactory())
        class NewEndpoint(Endpoint):
            """Documentation stringt"""

            path = 'new path'
            """Path"""

            method = 'HTTP Verb'
            """Method"""

            requires_shard = True  # Indicates whether the URL takes the SHARD or not
            """Requires Shard"""


3. If the URL (or query params) are particularly special, you may need to override `url` and/or `__call__` (see :class:`pubg_client.endpoints.Match` for an example of that).
4. Add a unit test file under `tests/unit/models/` if necessary, desirable.
5. Add a regression test in `tests/regression/test_ENDPOINT_NAME.py`
6. Consider adding an integration test in `tests/integration/test_ENDPOINT_NAME.py`
