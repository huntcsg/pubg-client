from collections import namedtuple
from json import JSONEncoder

import pendulum


class ModelEncoder(JSONEncoder):
    """Helper class for encoding objects as JSON"""
    def default(self, obj):
        """Call export on :class:`~pubg_client.models._base.Model` objects and
        :meth:`~pendulum.Pendulum.isoformat` on :class:`~pendulum.Pendulum` objects.

        :param obj: An object to encode as JSON
        :return: An object suitable to be recursively encoded as JSON
        """
        if isinstance(obj, Model):
            return obj.export()

        elif isinstance(obj, pendulum.Pendulum):
            return obj.isoformat()

        return JSONEncoder.default(obj)


Mapping = namedtuple('Mapping', ['pubg_key', 'cls'])
"""Mapping container"""


class Model:
    """Model base class"""

    key_map = {}
    """This is currently the 'magic' to this class. This should contain a mapping from pythonic
    attribute name to a :class:`~pubg_client.models._base.Mapping` object, which has the payload
    attribute and a callable that will be called on the value of that field. Although this might be
    a type, like :class:`str`, or :class:`dict`, it may also be a sublclass of
    :class:`~pubg_client.models._base.Model` or even a callable that returns some other type."""

    def __init__(self, **kwargs):
        """Given some keyword arguemnts, attach them to the instance as attributes
        Additionally set a `_resp` attribute that will get the raw :class:`~requests.Response` object
        that resulted in this model being created.

        :param kwargs: Any keyword arguments.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

        self._response = None

    def __call__(self, payload):
        """Allows any instance of this class to be a factory. This leads to a more developer friendly
        usage, allowing for the instantiation to take keyword arguements, but to have a calling
        convention similar to :class:`str`, :class:`int`, :class:`dict`, etc.

        :param payload: A data structure suitable for :meth:`load` to be called.
        :return: A :class:`~pubg_client.models._base.Model` instance
        """
        return self.load(payload)

    @classmethod
    def load(cls, payload):
        """Given a payload, typically a :class:`dict`, but possibly a :class;`list` or other object,
        return an instance of the :class:`~pubg_client.models._base.Model`.

        :param payload: A :class:`dict`
        :return: A :class:`~pubg_client.models._base.Model`
        """
        return cls(**{
            key: mapping.cls(payload[mapping.pubg_key])
            for key, mapping in cls.key_map.items()
        })

    def export(self):
        """

        :return:
        """
        exported = {}
        for key, mapping in self.key_map.items():
            if hasattr(mapping.cls, 'export'):
                exported[key] = getattr(self, key).export()
            elif isinstance(getattr(self, key), pendulum.Pendulum):
                exported[key] = getattr(self, key).isoformat()
            else:
                exported[key] = getattr(self, key)

        return exported

    def __repr__(self):
        return '{0.__class__.__name__}({1})'.format(
            self,
            ', '.join(
                '{}={}'.format(repr(key), repr(getattr(self, key, None)))
                for key in self.key_map.keys()
            )
        )


class PassThrough(Model):
    """Passthrough Model that can be used if there is an unknown set of keys"""

    key_map = {}

    def __init__(self, name, **kwargs):
        self._name = name
        super().__init__(**kwargs)

    def load(self, payload):
        instance = self.__class__(self._name, **payload)
        instance.key_map = {}
        for key, value in payload.items():
            instance.key_map[key] = Mapping(key, type(value))

        return instance

    def __repr__(self):
        return '{0._name}({1})'.format(
            self,
            ', '.join(
                '{}={}'.format(repr(key), repr(getattr(self, key)))
                for key in self.key_map.keys()
            )
        )


class List:
    """A list wrapper that returns a python list of Model objects"""

    def __init__(self, obj):
        self.obj = obj

    def __call__(self, payload):
        return [
            self.obj(item)
            for item in payload
        ]
