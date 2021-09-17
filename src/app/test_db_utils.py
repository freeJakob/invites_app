import asyncio
from typing import List, Dict, Any

from sqlalchemy import insert, delete

from src.app.db import database


def run_in_loop(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(func(*args, **kwargs))


async def execute_db_query(query):
    await database.execute(query)


def create_objects(model, values: List[Dict[str, Any]]):
    query = insert(model).values(values)
    run_in_loop(execute_db_query, query=query)


def flush_table(model):
    query = delete(model)
    run_in_loop(execute_db_query, query=query)