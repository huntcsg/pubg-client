**A python client for the pubg API**

|travis| |pypi| |docs|

Features:

    - Versioned API Endpoint and response payloads
    - Pagination Support

    .. DANGER::

       This library is in alpha. I will try my utmost to not make backwards incompatible changes
       but it is possible that they will be necessary.


Installing
----------

   .. code-block:: shell

      $ pip install pubg-client

Basic Usage
-----------

The `Client` is the main entrypoint of this library.

    :base_url: The URL to use. Defaults to https://api.playbattlegrounds.com
    :token: Pass this argument to add your token. If you don't include it, it won't be added to requests. All requests originating from this client will use this token.
    :shard: Pass this argument to set the client shard. Either update this to make requests to different shards, or make multiple client objects, one per shard. Client objects are pretty light, so having one per shard shouldn't be an issue.
    :raw: Pass this boolean if you want to get back raw python object responses instead of the deserialized versions (with useful python objects). This is False by default.
    :autocall: Pass this boolean if you want api methods to automatically emit requests. This is convenient, but needs to be turned off if you intend to utilize the method chaining for sorting/filtering/paging. It is off by default.


    .. code-block:: python

        import os
        from pubg_client import Client

        client = Client(
            token=os.environ['PUBG_API_KEY'],
            shard='xbox-na',
            raw=True,
            autocall=True
        )

        status = client.api.status()
        print(status)
        # {'type': 'status', 'id': 'pubg-api', 'attributes': {'releasedAt': '2018-03-12T14:08:16Z', 'version': 'master'}}

All api methods can be found as attributes on the `client.api` object. Currently they are:

    - status (:class:`pubg_client.endpoints.Status`)
    - match (:class:`pubg_client.endpoints.Match`)
    - matches (:class:`pubg_client.endpoints.Matches`)

Additionally, matches can be filtered, sorted, and paged thusly (See all the methods on :class:`~pubg_client._client.PUBGRequest`):

    .. code-block:: python

        from pubg_client import  Client
        client = Client(autocall=False)  # The default, but this is the required option

        matches_req = client.api.matches().sort('createdAt').filter('playerIds', 'mr-death-knell')
        print(matches)
        # <PUBGRequest(
        #       prepared_request=<[
        #           url=https://api.playbattlegrounds.com/shards/pc-na/matches,
        #           method=GET,
        #           params={'sort': 'createdAt', 'filter[playerIds]': 'mr-death-knell'}
        #       ]>,
        #       client_or_endpoint=Matches(deserializer=<class 'pubg_client.models.match.MatchCollection'>, client=<pubg_client._client.Client object at 0x105a04fd0>)
        # )>

        matches = matches_req()  # calling this object actually emits the web request and returns the deserialized result (in this case a MatchCollection)
        print(matches)
        # pubg_client.models.match.MatchCollection()  # In reality the repr would be more verbose


Development
-----------

   .. code-block:: shell

      $ git clone https://github.com/huntcsg/pubg-client.git
      $ cd pubg-client
      $ ./utils/manage clean
      $ ./utils/manage test
      $ ./utils/manage test-regression
      $ ./utils/manage docs


1. All pull requests must pass the travis-ci builds
2. All pull requests should include inline (docstring) documentation, updates to built documentation if applicable,
   and test coverage. This project aspires to be a 100% test coverage library.

Releases
--------

1. Open a pull request from the master branch into the v0 branch. Once this PR is merged, travis
   will automatically tag the release, upload the package to pypi and cherry pick the release commits
   back into the master branch.
2. Major version releases will require some re-work of the release scripts, but will generally be the same idea.

.. |travis| image:: https://travis-ci.org/huntcsg/pubg-client.svg?branch=master
   :target: https://travis-ci.org/huntcsg/pubg-client
.. |pypi| image:: https://img.shields.io/pypi/v/pubg-client.svg
   :target: https://pypi.python.org/pypi/pubg-client
.. |docs| image:: https://readthedocs.org/projects/pubg-client/badge/?version=latest
   :target: http://pubg-client.readthedocs.io/en/latest/?badge=latest
