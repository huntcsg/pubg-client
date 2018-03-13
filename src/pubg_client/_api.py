class API:
    """The api namespace"""

    def __init__(self, client, raw=False, autocall=False):
        """

        :param client:
        :param raw:
        :param autocall:
        """
        self.client = client
        self.raw = raw
        self.autocall = autocall

    @classmethod
    def register_endpoint(cls, name, deserializer, endpoint):
        """

        :param name:
        :param deserializer:
        :param endpoint:
        :return:
        """
        setattr(cls, name, endpoint(deserializer))

    @classmethod
    def register(cls, name, deserializer):
        """

        :param name:
        :param deserializer:
        :return:
        """
        def _register(endpoint):
            cls.register_endpoint(name, deserializer, endpoint)
            return endpoint
        return _register
