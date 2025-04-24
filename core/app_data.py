from sqlalchemy import create_engine
from settings import DATABASE_URL

from core.models import Base


class AppData:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine)
