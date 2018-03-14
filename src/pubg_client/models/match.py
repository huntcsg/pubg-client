import pendulum

from ._base import List, Mapping, Model
from .asset import Asset
from .roster import Roster


class Match(Model):
    """A match object. Click 'source' to see the key map for this Model."""

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

    def __init__(self, matches):
        super().__init__()
        self._matches = matches

    @classmethod
    def load(cls, payload):
        return cls(matches=[Match(item) for item in payload])

    def __iter__(self):
        return iter(self._matches)

    def __len__(self):
        return len(self._matches)

    def next_page(self, client):
        response = self._response
        new_response = client.next_page(response)
        new_result = self.__class__.load(new_response.json().get('data', []))
        new_result._response = new_response
        return new_result

    def previous_page(self, client):
        response = self._response
        new_response = client.previous_page(response)
        new_result = self.__class__.load(new_response.json().get('data', []))
        new_result._response = new_response
        return new_result
