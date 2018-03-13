Adding a New Model
------------------

1. Find or create a new python module under `src/pubg_client/models/`

    .. code-block:: python

        from ._base import Mapping, Model


        class NewModel(Model):

            key_map = {
                'key': Mapping('key_in_api', type)
            }

2. If needed, define a `load`, `next`, and `previous` method.
3. If appropriate, register it as the deserializer for an endpoint (or in another models key map)