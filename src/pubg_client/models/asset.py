from ._base import Mapping, Model


class Asset(Model):
    """Asset objects contain a URL string that links to a telemetry.json file, which will contain an array of event objects that provide further insight into a match."""

    key_map = {
        'id': Mapping('id', str),
        'title_id': Mapping('titleId', str),
        'shard_id': Mapping('shardId', str),
        'name': Mapping('name', str),
        'description': Mapping('description', str),
        'createdAt': Mapping('description', str),
        'filename': Mapping('filename', str),
        'content_type': Mapping('contentType', str),
        'url': Mapping('URL', str),
    }


class AssetCollection(Model):
    """A collection of assets"""

    @classmethod
    def load(cls, payload):
        return [
            Asset(obj)
            for obj in payload
        ]
