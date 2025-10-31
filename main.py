from oxapy import HttpServer, SessionStore
from oxapy import templating

from core.routers import pub_router, sec_router

from settings import TEMPLATE_DIR


if __name__ == "__main__":
    (
        HttpServer(("0.0.0.0", 8000))
        .session_store(SessionStore())
        .template(templating.Template(TEMPLATE_DIR))
        .attach(pub_router)
        .attach(sec_router)
        .run()
    )
