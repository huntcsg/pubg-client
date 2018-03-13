from collections import namedtuple
from json import JSONEncoder

import pendulum


class ModelEncoder(JSONEncoder):
    """Helper class for encoding objects as JSON"""
    def default(self, obj):
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

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

        self._resp = None

    def __call__(self, payload):
        """

        :param payload:
        :return:
        """
        return self.load(payload)

    @classmethod
    def load(cls, payload):
        """

        :param payload:
        :return:
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
