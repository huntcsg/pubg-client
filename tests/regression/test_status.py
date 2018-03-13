from pubg_client import Client
import requests_mock
import json
from .responses.status import responses
import pytest


class TestStatus:

    @pytest.mark.parametrize(
        'response,', responses,
        ids=[
            resp['id']
            for resp in responses
        ],
    )
    def test_raw(self, response):
        with requests_mock.mock() as m:
            m.get('https://api.playbattlegrounds.com/status', text=response['text'])
            client = Client(raw=True, autocall=True)
            status = client.api.status()

        assert status == json.loads(response['text'])['data']
