from sqlalchemy import create_engine
from settings import TURSO_DATABASE_URL, TURSO_AUTH_TOKEN
from core.models import Base

ENGINE = create_engine(
    "sqlite+libsql:///replicate.db",
    connect_args={
        "auth_token": TURSO_AUTH_TOKEN,
        "sync_url": TURSO_DATABASE_URL,
    },
)
Base.metadata.create_all(ENGINE)


class AppData:
    global ENGINE

    def __init__(self):
        self.engine = ENGINE
