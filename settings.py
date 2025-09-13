from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.models import Base
from core.repositories import create_user

load_dotenv()

TURSO_DATABASE_URL = getenv("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = getenv("TURSO_AUTH_TOKEN")
MAIL_TRAP_TOKEN = getenv("MAIL_TRAP_TOKEN")
TEMPLATE_DIR = "templates/**/*.j2"

ENGINE = create_engine(
    "sqlite+libsql:///replicate.db",
    connect_args={
        "auth_token": TURSO_AUTH_TOKEN,
        "sync_url": TURSO_DATABASE_URL,
    },
)

DB = sessionmaker(bind=ENGINE)


def create_user_manually(name: str, email: str, password: str):
    with Session(ENGINE) as session:  # type: ignore
        create_user(session, name, email, password)
