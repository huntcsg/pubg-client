"""Client Module"""
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
"""Shards"""


class Client:
    """The client class"""

    def __init__(self, base_url='https://api.playbattlegrounds.com', token=None, shard='pc-na', raw=False, autocall=False):
        """

        :param base_url:
        :param token:
        :param shard:
        :param raw:
        :param autocall:
        """
        self.base_url = base_url
        self.token = token if token is not None else ''
        self.shard = self.validate_shard(shard)
        self.raw = raw
        self.session_factory = requests.Session
        self.autocall = autocall

    def prepare_request(self, method, url, gzip=False, **kwargs):
        """

        :param method:
        :param url:
        :param gzip:
        :param kwargs:
        :return:
        """

        header = {
            "Authorization": self.token,
            "Accept": "application/vnd.api+json",
        }

        if gzip:
            header["Accept-Encoding"] = "gzip"

        return PUBGRequest(requests.Request(method, url, headers=header, **kwargs), self)

    def make_request(self, request):
        """

        :param request:
        :return:
        """
        s = self.session_factory()
        return s.send(request.prepare())

    def request(self, method, url, **kwargs):
        """

        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        req = self.prepare_request(method, url, **kwargs)
        return self.make_request(req)

    def next_page(self, response):
        """

        :param response:
        :return:
        """
        return self.request('GET', response.json()['links']['next'])

    def previous_page(self, response):
        """

        :param response:
        :return:
        """
        return self.request('GET', response.json()['links']['last'])

    def current_page(self, response):
        """

        :param response:
        :return:
        """
        return self.request('GET', response.json()['links']['self'])

    def get_token(self, token=None):
        """

        :param token:
        :return:
        """
        if token is not None:
            return token
        elif self.token is not None:
            return self.token
        else:
            return ''

    def get_shard(self, shard=None):
        """

        :param shard:
        :return:
        """
        shard = shard if shard is not None else self.shard
        self.validate_shard(shard)
        return shard

    def validate_shard(self, shard):
        """

        :param shard:
        :return:
        """
        if shard in SHARDS:
            return shard
        else:
            raise ValueError('shard not found! {shard}'.format(shard=shard))

    @property
    def api(self):
        """

        :return:
        """
        return API(client=self, raw=self.raw, autocall=self.autocall)


class PUBGRequest:
    """A lazy request object

    """

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
