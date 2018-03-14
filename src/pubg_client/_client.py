"""The _client module contains classes and constants related to making actual web requests to the api.
Additionally, it exposes some configuration that gets passed into the API and Endpoint objects.

It comes with some sane defaults, so making requests can be as simple as:

    >>> from pubg_client import Client
    >>> client = Client()

"""
import requests

from ._api import API
from .endpoints._base import Endpoint

SHARDS = {
    'xbox-as': 'xbox-Asia',
    'xbox-eu': 'xbox-Europe',
    'xbox-na': 'xbox-North America',
    'xbox-oc': 'xbox-Oceania',
    'pc-krjp': 'pc-Korea/Japan',
    'pc-na': 'pc-North America',
    'pc-eu': 'pc-Europe',
    'pc-oc': 'pc-Oceania',
    'pc-kakao': 'pc-kakao',
    'pc-sea': 'pc-South East Asia',
    'pc-sa': 'pc-South and Central America',
    'pc-as': 'pc-Asia',
}
"""Known Shards. If needed, more can be added or removed at runtime to manage which are valid."""


class Client:

    def __init__(self, base_url='https://api.playbattlegrounds.com', token=None, shard='pc-na', raw=False, autocall=False):
        """The client class itself holds the token and shard to be used for requests.

        It also exposes an attribute: `session_factory` to customize the requests session that is used (for example to modify timeouts).

        :param base_url: A :class:`str` url.
        :param token: A :class:`str` jwt token
        :param shard: A :class:`str` shard that requests should be made against
        :param raw: A :class:`bool` indicating whether responses should be deserialized into python objects or left as simple dictionaries, etc.
        :param autocall: A :class:`bool` indicating whether to return :class:`~pubg_client._client.PUBGRequest` objects from api method calls or to automatically make the requests.
        This must be `False` in order to do method chaining for filtering and sorting.
        """
        self.base_url = base_url
        self.token = token if token is not None else ''
        self.shard = self.validate_shard(shard)
        self.raw = raw
        self.autocall = autocall

        self.session_factory = requests.Session
        """The session factory. This can be overridden and will be called with no arguments whenever requests are made."""

    def prepare_request(self, method, url, gzip=False, **kwargs):
        """Given a method, URL, and a variaty of arguments, returns a :class:`~pubg_client._client.PUBGRequest` object that contains a :class:`requests.Request` prepared request and a reference to this client.

        :param method: A :class:`str` HTTP verb
        :param url: A :class:`str` URL
        :param gzip: A :class:`bool` indicating whether to gzip the response or not.
        :param kwargs: Any additional keyword arguments that will get passed into the :class:`requests.Request` call.
        :return: A :class:`~pubg_client._client.PUBGRequest` object.
        """
        header = {
            'Accept': 'application/vnd.api+json'
        }

        if self.token:
            header['Authorization'] = self.token

        if gzip:
            header['Accept-Encoding'] = 'gzip'

        return PUBGRequest(requests.Request(method, url, headers=header, **kwargs), self)

    def make_request(self, request):
        """Create a session and send the prepared request, returning the :class:`~requests.Response` object.

        :param request: A :class:`~requests.Request` object
        :return: A :class:`~requests.Response` object
        """
        s = self.session_factory()
        return s.send(request.prepare())

    def request(self, method, url, **kwargs):
        """A convenience method that takes a method and url and prepares and makes the request.

        :param method: A :class:`str` HTTP verb
        :param url: A :class:`str` URL
        :param kwargs: Any keyword arguments that will be passed into the `~requests.Request` call.
        :return: A :class:`~requests.Response` object
        """
        req = self.prepare_request(method, url, **kwargs)
        return self.make_request(req)

    def next_page(self, response):
        """Request the next page of results from a response containing a link key in the json response.

        :param response: A :class:`requests.Response` object
        :return: A :class:`requests.Response` object
        """
        return self.request('GET', response.json()['links']['next'])

    def previous_page(self, response):
        """Request the previous page of results from a response containing a link key in the json response.

        :param response: A :class:`requests.Response` object
        :return: A :class:`requests.Response` object
        """
        return self.request('GET', response.json()['links']['last'])

    def current_page(self, response):
        """

        :param response: A :class:`requests.Response` object
        :return: A :class:`requests.Response` object
        """
        return self.request('GET', response.json()['links']['self'])

    def get_token(self, token=None):
        """Given a string token or None, returns the given token, the token attached to the object, or an empty string.

        :param token: A :class`str` jwt token
        :return: A :class:`str`
        """
        if token is not None:
            return token
        elif self.token is not None:
            return self.token
        else:
            return ''

    def get_shard(self, shard=None):
        """Given a shard :class:`str`, validates it is in the `SHARD` constant. Defaults to the shard attached to `self`.

        :raises ValueError: If the shard is not in the SHARDS constant
        :param shard: A :class:`str` shard
        :return: the :class:`str` shard
        """
        shard = shard if shard is not None else self.shard
        self.validate_shard(shard)
        return shard

    def validate_shard(self, shard):
        """Validates the shard is in the SHARDS

        :raises ValueError: if the shard is not in the SHARDS constant
        :param shard: A :class:`str` shard
        :return: None
        """
        if shard in SHARDS:
            return shard
        else:
            raise ValueError('shard not found! {shard}'.format(shard=shard))

    @property
    def api(self):
        """Create a fresh API instance each time this is called. This prevents any caching in the API class. Options in the client will always be reflected
        if the api object is used from the :class:`~pubg_client._client.CLient` object.

        :return: An :class:`~pubg_client._api.API` instance with the proper options from the :class:`~pubg_client._client.CLient` object.
        """
        return API(client=self, raw=self.raw, autocall=self.autocall)


class PUBGRequest:
    """A lazy request object"""

    def __init__(self, prepared_request, client_or_endpoint):
        """

        :param prepared_request:
        :param client_or_endpoint:
        """
        self.prepared_request = prepared_request
        self.client_or_endpoint = client_or_endpoint

    def filter(self, filter_name, filter_value):
        """

        :param filter_name:
        :param filter_value:
        :return:
        """
        self._add_filter(self.prepared_request, filter_name, filter_value)
        return self

    def sort(self, sort_key):
        """

        :param sort_key:
        :return:
        """
        self._add_sorting(self.prepared_request, sort_key)
        return self

    def limit(self, limit):
        """

        :param limit:
        :return:
        """
        self._add_page_limit(self.prepared_request, limit)
        return self

    def offset(self, offset):
        """

        :param offset:
        :return:
        """
        self._add_page_offset(self.prepared_request, offset)

    @staticmethod
    def _add_page_limit(request, limit):
        """

        :param request:
        :param limit:
        :return:
        """
        params = {
            'page[limit]': limit,
        }

        request.params.update(params)

    @staticmethod
    def _add_page_offset(request, offset):
        """

        :param request:
        :param offset:
        :return:
        """
        params = {
            'page[offset]': offset,
        }
        request.params.update(params)

    @staticmethod
    def _add_sorting(request, sort_key):
        """

        :param request:
        :param sort_key:
        :return:
        """
        params = {
            'sort': sort_key,
        }
        request.params.update(params)

    @staticmethod
    def _add_filter(request, filter_name, filter_value):
        """

        :param request:
        :param filter_name:
        :param filter_value:
        :return:
        """
        params = {
            'filter[{filter_name}]'.format(filter_name=filter_name): filter_value
        }
        request.params.update(params)

    def __call__(self, client_or_endpoint=None):
        """

        :param client_or_endpoint:
        :return:
        """
        client_or_endpoint = client_or_endpoint if client_or_endpoint is not None else self.client_or_endpoint

        if isinstance(client_or_endpoint, Client):
            return client_or_endpoint.make_request(self.prepared_request)
        elif isinstance(client_or_endpoint, Endpoint):
            return client_or_endpoint.request(self.prepared_request)
        else:
            raise TypeError("PUBGRequest doesn't know how to use <{}> to make a request!".format(str(client_or_endpoint)))

    def __repr__(self):
        return '<PUBGRequest(prepared_request=<[ url={}, method={}, params={}]>, client_or_endpoint={})>'.format(self.prepared_request.url, self.prepared_request.method, self.prepared_request.params, repr(self.client_or_endpoint))
