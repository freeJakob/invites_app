from datetime import datetime

from src.app.models import Users, BoardingPasses
from src.app.test_db_utils import create_objects, flush_table

users = [
    {
        'name': 'user_1',
        'distance': 1,
        'hours': 2,
    },
]
boarding_passes = [
    {
        'user_id': 1,
        'destination': 'dest 1',
        'address': 'addr 1',
        'boarding_datetime': '2021-01-01 06:30',
        'checked_in': False,
        'code': '123',
        'checked_at': datetime.now()
    },
]


def test_check_in(api_client):
    create_objects(Users, users)
    create_objects(BoardingPasses, boarding_passes)

    response = api_client.post(
        '/api/boarding_passes/check_in/',
        json={'value': 123},
    )
    assert response.status_code == 200
    assert response.json()['username'] == users[0]['name']

    response = api_client.post(
        '/api/boarding_passes/check_in/',
        json={'value': 123},
    )

    assert response.status_code == 400
    assert response.json()['detail'] == 'Already checked in'

    flush_table(Users)
    flush_table(BoardingPasses)


def test_boarding_ws(api_client):
    create_objects(Users, users)
    create_objects(BoardingPasses, boarding_passes)

    with api_client.websocket_connect("/boarding/ws") as ws:
        data = ws.receive_json()
        assert data == {}
        response = api_client.post(
            '/api/boarding_passes/check_in/',
            json={'value': 123},
        )
        assert response.status_code == 200
        data = ws.receive_json()
        assert data == {'id': 1, 'name': 'user_1', 'distance': 1, 'hours': 2}

    flush_table(Users)
    flush_table(BoardingPasses)
