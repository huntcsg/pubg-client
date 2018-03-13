Get Matches
-----------

Get some matches:

   .. code-block:: python

        from pubg_client import Client
        import os

        client = Client(token=os.environ['PUBG_API_KEY'], autocall=True)
        matches = client.api.matches()


Get the next matches:

   .. code-block:: python

        from pubg_client import Client
        import os

        client = Client(token=os.environ['PUBG_API_KEY'], autocall=True)
        matches = client.api.matches()

        next_matches = matches.next(client)


