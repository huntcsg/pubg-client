from ..models._base import PassThrough


class Endpoint:
    """The endpoint class"""
    requires_shard = False

    def __init__(self, deserializer=None, client=None):
        """

        :param deserializer:
        :param client:
        """

        if deserializer is None:
            deserializer = PassThrough(name=self.__class__.__name__)

        self.deserializer = deserializer
        self.client = client
        self.autocall = False
        self.raw = False

    def __get__(self, instance, cls):
        """Allows the endpoint to grab useful information from the API container (and client)"""
        self.client = instance.client
        self.raw = instance.raw
        self.autocall = instance.autocall
        return self

    def url(self):
        """

        :return:
        """
        if self.requires_shard:
            return '{base_url}/shards/{shard}/{path}'.format(base_url=self.client.base_url, path=self.path, shard=self.client.shard)
        else:
            return '{base_url}/{path}'.format(base_url=self.client.base_url, path=self.path)

    def request(self, prepared_request):
        """

        :param prepared_request:
        :return:
        """
        response = self.client.make_request(prepared_request)

        if not response.ok:
            return self.handle_error(response)

        if not self.raw:
            resp = self.deserializer.load(response.json().get('data', {}))
            resp._response = response
            return resp
        else:
            return response.json().get('data', {})

    def __repr__(self):
        return '{0.__class__.__name__}(deserializer={1}, client={2})'.format(
            self,
            repr(self.deserializer.__class__),
            repr(self.client),
        )

    def handle_error(self, response):
        """Allows for endpoint specific error handling

        :param response:
        :return:
        """
        response.raise_for_status()

    def __call__(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        url = self.url()
        prepared_request = self.client.prepare_request(self.method, url, **kwargs)
        prepared_request.client_or_endpoint = self
        if self.autocall:
            return prepared_request()
        else:
            return prepared_request
