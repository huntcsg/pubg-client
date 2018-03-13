from .._api import API
from ..models import match
from ._base import Endpoint


@API.register('matches', match.MatchCollection())
class Matches(Endpoint):
    """Matches Endpoint"""

    path = 'matches'
    """Path"""

    method = 'GET'
    """Method"""

    requires_shard = True
    """Requires Shard"""


@API.register('match', match.Match())
class Match(Endpoint):
    path = 'matches/{id}'
    """Path"""

    method = 'GET'
    """Method"""

    requires_shard = True
    """Requires Shard"""

    def url(self, id):
        """

        :param id:
        :return:
        """
        return super().url().format(id=id)

    def __call__(self, id, **kwargs):
        """

        :param id:
        :param kwargs:
        :return:
        """
        url = self.url(id=id)
        prepared_request = self.client.prepare_request(self.method, url, **kwargs)
        prepared_request.client_or_endpoint = self
        if self.autocall:
            return prepared_request()
        else:
            return prepared_request
