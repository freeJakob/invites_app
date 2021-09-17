import os
from datetime import datetime, timedelta

from src.app.config import BP_IMAGES_STORAGE
from src.app.models import Users, BoardingPasses
from src.app.test_db_utils import create_objects, flush_table

users = [
    {
        'name': 'user_1',
        'distance': 1,
        'hours': 2,
    },
    {
        'name': 'user_2',
        'distance': 3,
        'hours': 4,
    },
]
boarding_passes = [
    {
        'user_id': 1,
        'destination': 'dest 1',
        'address': 'addr 1',
        'boarding_datetime': '2021-01-01 06:30',
        'checked_in': True,
        'code': 123,
        'checked_at': datetime.now()
    },
    {
        'user_id': 2,
        'destination': 'dest 2',
        'address': 'addr 2',
        'boarding_datetime': '2021-01-01 06:30',
        'checked_in': False,
        'code': 321,
        'checked_at': datetime.now() + timedelta(hours=1)
    }
]


def test_users_list_latest(api_client):
    create_objects(Users, users)
    create_objects(BoardingPasses, boarding_passes)

    response = api_client.get("/api/users/list_arrived/")
    assert response.status_code == 200
    assert len(response.json()) == 1

    flush_table(Users)
    flush_table(BoardingPasses)


def test_users_empty_db(api_client):
    response = api_client.get("/api/users/list_arrived/")
    assert response.status_code == 200
    assert response.json() == []


def test_gen_bp_image(api_client):
    create_objects(Users, users)
    payload = {
        "destination": "SPB",
        "boarding_datetime": "2020-01-01 06:30",
        "address": "aeroport"
    }
    response = api_client.post(
        '/api/users/1/generate_pass/',
        json=payload
    )

    assert response.status_code == 200

    assert os.path.isfile(
        f'{BP_IMAGES_STORAGE}/'
        f'bp_{payload["destination"]}_{payload["boarding_datetime"]}.png',
    )

    flush_table(Users)
    flush_table(BoardingPasses)
