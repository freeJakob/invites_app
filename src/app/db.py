import os

import databases
from dotenv import load_dotenv
from sqlalchemy import create_engine

from src.app import models

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '..', ".env"))


if os.environ.get('TESTING'):
    database = databases.Database("sqlite:///./test.db", force_rollback=True)
    engine = create_engine(
        "sqlite:///./test.db", connect_args={"check_same_thread": False}
    )
    models.Base.metadata.create_all(engine)
else:
    database = databases.Database(os.environ["DATABASE_URL"])


