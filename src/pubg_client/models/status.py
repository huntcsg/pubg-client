import pendulum

from ._base import Mapping, Model


class StatusAttributes(Model):
    """A status attributes object. This is so that we can parse the released at string into a Datetime"""

    key_map = {
        'released_at': Mapping('releasedAt', pendulum.parse),
        'version': Mapping('version', str)
    }


class Status(Model):
    """A status"""
    key_map = {
        'id': Mapping('id', str),
        'type': Mapping('type', str),
        'attributes': Mapping('attributes', StatusAttributes()),
    }

    @property
    def released_at(self):
        """Convenience Method"""
        return self.attributes.released_at

    @property
    def version(self):
        """Convenience Method"""
        return self.attributes.version
