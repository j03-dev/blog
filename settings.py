from os import getenv
from dotenv import load_dotenv


load_dotenv()

TURSO_DATABASE_URL = getenv("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = getenv("TURSO_AUTH_TOKEN")
TEMPLATE_DIR = "templates/**/*.j2"
