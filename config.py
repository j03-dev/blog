from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()

TURSO_DATABASE_URL = getenv("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = getenv("TURSO_AUTH_TOKEN")
TEMPLATE_DIR = "templates/**/*.j2"

ENGINE = create_engine(
    "sqlite+libsql:///replicate.db",
    connect_args={
        "auth_token": TURSO_AUTH_TOKEN,
        "sync_url": TURSO_DATABASE_URL,
    },
)

DB = sessionmaker(bind=ENGINE)
