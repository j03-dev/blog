from oxapy import HttpServer, SessionStore
from oxapy import templating
from sqlalchemy.orm import Session

from core.routers import pub_router, sec_router
from core.app_data import AppData, ENGINE
from core.repositories import create_user

from settings import TEMPLATE_DIR


def create_user_manually(name: str, email: str, password: str):
    with Session(ENGINE) as session:  # type: ignore
        create_user(session, name, email, password)


server = HttpServer(("0.0.0.0", 8000))
server.app_data(AppData())
server.session_store(SessionStore())
server.template(templating.Template(TEMPLATE_DIR))
server.attach(pub_router)
server.attach(sec_router)

if __name__ == "__main__":
    server.run()
