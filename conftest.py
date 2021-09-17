from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import insert

from src.app.main import app
from src.app.db import database
from src.app.models import Users, BoardingPasses


@pytest.fixture(scope="session")
def api_client():
    client = TestClient(app)

    return client


