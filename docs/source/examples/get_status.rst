Get Status
----------

   .. code-block:: python

        from pubg_client import Client

        client = Client(autocall=True)

        status = client.api.status()

        print(status)
        print(status.version)
        print(status.released_at)

