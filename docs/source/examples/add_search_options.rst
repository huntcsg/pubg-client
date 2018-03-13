Add Search Options
------------------

Do some sorting

   .. code-block:: python

        from pubg_client import Client
        import os

        client = Client(token=os.environ['PUBG_API_KEY'], autocall=False)
        prepared_request = client.api.matches().sort('createdAt')
        matches = prepared_request()


Filter the matches (and sort)

   .. code-block:: python

        from pubg_client import Client
        import os

        client = Client(token=os.environ['PUBG_API_KEY'], autocall=False)
        prepared_request = client.api.matches().sort('createdAt').filter('createdAt', '2018-04-01T00:01:01Z')
        matches = prepared_request()


