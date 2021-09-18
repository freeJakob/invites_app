import secrets
from datetime import datetime
from operator import eq
from typing import Dict, Tuple

from PIL import Image, ImageFont, ImageDraw
from fastapi import APIRouter, HTTPException, BackgroundTasks
from sqlalchemy import select, insert

from src.api.const import API_ENDPOINT, HTTP_400_BAD_REQUEST
from src.api.schemas import BPInfo
from src.app.config import STATIC_FOLDER, BP_IMAGES_STORAGE
from src.app.db import database
from src.app.models import Users, BoardingPasses

users_router = APIRouter()

USERS_ENDPOINT = 'users'
BP_FONT_28 = ImageFont.truetype(f'{STATIC_FOLDER}/fonts/futura.ttf', 28)
BP_FONT_20 = ImageFont.truetype(f'{STATIC_FOLDER}/fonts/futura.ttf', 20)
BP_FONT_12 = ImageFont.truetype(f'{STATIC_FOLDER}/fonts/futura.ttf', 12)
BP_FONT_10 = ImageFont.truetype(f'{STATIC_FOLDER}/fonts/futura.ttf', 10)
BLACK_RGB = (0, 0, 0)
WHITE_RGB = (255, 255, 255)


@users_router.get('/%s/%s/list_arrived/' % (API_ENDPOINT, USERS_ENDPOINT))
async def list_checked_in_users():
    checked_bp_query = select(
        from_obj=BoardingPasses,
        columns=[Users.id, Users.name, Users.distance, Users.hours]
    ).where(
        eq(BoardingPasses.checked_in, True)
    ).join(
        Users, BoardingPasses.user_id == Users.id
    )
    checked_in_users = await database.fetch_all(checked_bp_query)

    if checked_in_users is None:
        return []

    return checked_in_users


@users_router.post(
    '/%s/%s/{user_id}/generate_pass/' % (API_ENDPOINT, USERS_ENDPOINT)
)
async def generate(user_id: int, bp_info: BPInfo, bg_tasks: BackgroundTasks):
    user = await _get_user(user_id)
    if not await _is_bp_created(user_id, bp_info):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'Boarding Pass for user: {user["name"]} already created'
        )
    boarding_code = secrets.token_hex(4)
    await _create_bp(user_id, bp_info, boarding_code)
    bg_tasks.add_task(_generate_bp_image, bp_info, user, boarding_code)

    return user


async def _is_bp_created(user_id: int, bp_info: BPInfo) -> bool:
    query_parameters = bp_info.dict()
    query_parameters.update({'user_id': user_id})
    bp_query = select(BoardingPasses).where(
        *[
            eq(getattr(BoardingPasses, k), v)
            for k, v in query_parameters.items()
        ]
    )
    bps = await database.fetch_all(bp_query)
    if bps:
        return False

    return True


async def _create_bp(user_id: int, bp_info: BPInfo, boarding_code: str):
    bp_obj = bp_info.dict()
    bp_obj['user_id'] = user_id
    bp_obj['code'] = boarding_code

    query = insert(BoardingPasses).values([bp_obj])

    await database.execute(query)


async def _get_user(user_id: int) -> Dict[str, str]:
    users_query = select(Users).where(Users.id == user_id)
    user = dict(await database.fetch_one(users_query))

    return user


def _generate_bp_image(bp_info: BPInfo, user: Dict[str, str], boarding_code: str):
    bp_template = Image.open(
        f'{STATIC_FOLDER}/images/boarding_pass_template.png',
    )
    bp_template_editable = ImageDraw.Draw(bp_template)
    boarding_date, boarding_time = _parse_date_str(bp_info.boarding_datetime)

    bp_template_editable.text(
        (14, 95), user['name'], BLACK_RGB, font=BP_FONT_20,
    )
    bp_template_editable.text(
        (460, 35), user['name'], WHITE_RGB, font=BP_FONT_20,
    )

    bp_template_editable.text(
        (15, 155), bp_info.destination.upper(), BLACK_RGB, font=BP_FONT_12,
    )
    bp_template_editable.text(
        (460, 80), bp_info.destination.upper(), WHITE_RGB, font=BP_FONT_12,
    )

    bp_template_editable.text(
        (180, 155), boarding_date, BLACK_RGB, font=BP_FONT_10,
    )
    bp_template_editable.text(
        (280, 155), boarding_time, BLACK_RGB, font=BP_FONT_10,
    )

    bp_template_editable.text(
        (460, 145), boarding_date, WHITE_RGB, font=BP_FONT_10,
    )
    bp_template_editable.text(
        (550, 145), boarding_time, WHITE_RGB, font=BP_FONT_10,
    )

    bp_template_editable.text(
        (250, 15), boarding_code, BLACK_RGB, font=BP_FONT_28,
    )
    bp_template_editable.text(
        (250, 50), bp_info.address, BLACK_RGB, font=BP_FONT_10,
    )

    bp_template.save(
        f'{BP_IMAGES_STORAGE}/'
        f'bp_{bp_info.destination}_{bp_info.boarding_datetime}.png'
    )


def _parse_date_str(datetime_str: str) -> Tuple[str, str]:
    boarding_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
    boarding_date = boarding_datetime.date().strftime('%Y / %m / %d')
    boarding_time = boarding_datetime.time().strftime('%I:%M %p')

    return boarding_date, boarding_time


@users_router.get('/%s/%s/make_test_user_and_bp/' % (API_ENDPOINT, USERS_ENDPOINT))
async def create_test_objects():
    user = {
        'name': 'test user',
        'distance': 1111,
        'hours': 2222,
    }
    bp = {
        'user_id': 1,
        'destination': 'dest 1',
        'address': 'addr 1',
        'boarding_datetime': '2021-01-01 06:30',
        'checked_in': False,
        'code': '123',
        'checked_at': datetime.now()
    }

    await database.execute(insert(Users).values([user]))
    await database.execute(insert(BoardingPasses).values([bp]))

    return {
        'user': user,
        'bp': bp,
    }
