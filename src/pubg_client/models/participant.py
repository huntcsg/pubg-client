from ._base import List, Mapping, Model


class Participant(Model):
    """A participant object. Click 'source' to see the key map for this Model."""

    key_map = {
        'id': Mapping('id', str),
        'stats': Mapping('stats', dict),
        'actor': Mapping('actor', str),
        'shard_id': Mapping('shardId', str),
    }
