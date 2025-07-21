from oxapy import HttpServer, SessionStore
from oxapy import templating

from core.routers import pub_router, sec_router

from settings import AppData, TEMPLATE_DIR


server = HttpServer(("0.0.0.0", 8000))
server.app_data(AppData())
server.session_store(SessionStore())
server.template(templating.Template(TEMPLATE_DIR))
server.attach(pub_router)
server.attach(sec_router)

if __name__ == "__main__":
    server.run()
