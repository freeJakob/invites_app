import json
import secrets
from datetime import datetime
from operator import eq
from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from fastapi import WebSocket
from sqlalchemy import select, update
from starlette.websockets import WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError

from src.api.const import API_ENDPOINT, HTTP_400_BAD_REQUEST
from src.api.schemas import CheckInCode
from src.api.users import _get_user
from src.app.db import database
from src.app.models import BoardingPasses, Users

bp_router = APIRouter()
BP_ENDPOINT = 'boarding_passes'

ESTABLISHED_WEBSOCKETS: Dict[str, WebSocket] = {}


@bp_router.post('/%s/%s/check_in/' % (API_ENDPOINT, BP_ENDPOINT))
async def check_in(check_in_code: CheckInCode):
    bp = await _get_bp(check_in_code)
    if bp['checked_in']:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Already checked in',
        )

    bp['checked_in'] = True
    bp['checked_at'] = datetime.now()
    await _update_bp(bp)
    user = await _get_user(bp['user_id'])

    await _trigger_established_sockets(user)

    return {
        'username': user['name'],
        'id': user['id'],
    }


@bp_router.websocket_route('/boarding/ws')
async def check_in(websocket: WebSocket):
    await websocket.accept()
    websocket_key = secrets.token_hex(16)
    ESTABLISHED_WEBSOCKETS[websocket_key] = websocket

    bp_query = select(
        from_obj=BoardingPasses,
        columns=[Users.id, Users.name, Users.distance, Users.hours]
    ).where(
        eq(BoardingPasses.checked_in, True)
    ).order_by(
        BoardingPasses.checked_at.asc(),
    ).join(
        Users, BoardingPasses.user_id == Users.id
    ).limit(1)
    latest_checked_user = await database.fetch_one(bp_query)
    if latest_checked_user is None:
        latest_checked_user = {}

    user_str = json.dumps(
        dict(latest_checked_user),
        indent=4,
        sort_keys=True,
        default=str,
    )
    await websocket.send_text(user_str)
    try:
        while True:
            data = await websocket.receive_json()
            await websocket.send_json(data)
    except WebSocketDisconnect:
        ESTABLISHED_WEBSOCKETS.pop(websocket_key)


async def _get_bp(code: CheckInCode) -> Dict[str, Any]:
    query = select(BoardingPasses).where(BoardingPasses.code == code.value)
    bp = dict(await database.fetch_one(query))

    if not bp:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Boarding pass with such code does not exist'
        )

    return bp


async def _update_bp(bp_obj: Dict[str, Any]):
    query = (
        update(BoardingPasses)
        .where(BoardingPasses.id == bp_obj['id'])
        .values(**bp_obj)
    )
    await database.execute(query)


async def _trigger_established_sockets(data: Dict[str, Any]):
    closed_websockets = []
    for key, socket in ESTABLISHED_WEBSOCKETS.items():
        try:
            await socket.send_json(data)
        except ConnectionClosedError:
            closed_websockets.append(key)

    for key in closed_websockets:
        ESTABLISHED_WEBSOCKETS.pop(key, None)
