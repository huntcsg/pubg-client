from ._base import List, Mapping, Model
from .participant import Participant


class Roster(Model):
    """A roster object"""

    key_map = {
        'id': Mapping('id', str),
        'team': Mapping('team', str),
        'participants': Mapping('participants', List(Participant())),
        'stats': Mapping('stats', dict),
        'won': Mapping('won', str),
        'shard_id': Mapping('shardId', str),
    }
