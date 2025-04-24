from oxapy import HttpServer
from oxapy import templating
from settings import TEMPLATE_DIR
from core.routers import pub_router
from core.app_data import AppData

server = HttpServer(("0.0.0.0", 8000))
server.app_data(AppData())
server.template(templating.Template(TEMPLATE_DIR))
server.attach(pub_router)

if __name__ == "__main__":
    server.run()
