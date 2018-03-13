import pendulum

from ._base import List, Mapping, Model
from .asset import Asset, AssetCollection
from .roster import Roster


class Match(Model):
    """A match object"""

    key_map = {
        'id': Mapping('id', str),
        'created_at': Mapping('createdAt', pendulum.parse),
        'duration': Mapping('duration', int),
        'rosters': Mapping('rosters', Roster),
        'rounds': Mapping('rounds', dict),
        'assets': Mapping('assets', List(Asset())),
        'spectators': Mapping('spectators', dict),
        'stats': Mapping('stats', dict),
        'game_mode': Mapping('gameMode', str),
        'patch_version': Mapping('patchVersion', str),
        'title_id': Mapping('titleId', str),
        'shard_id': Mapping('shardId', str),
        'tags': Mapping('tags', dict),
    }


class MatchCollection(Model):
    """A collection of matches with navigation conveninece methods"""

    @classmethod
    def load(cls, payload):
        data = payload['data']
        return super().load(data)

    def next(self):
        pass
