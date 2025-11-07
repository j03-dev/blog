from oxapy import HttpServer, SessionStore
from oxapy import templating

from core.routers import pub_router, sec_router

from settings import TEMPLATE_DIR

app = HttpServer(("0.0.0.0", 8000))
app.session_store(SessionStore())
app.template(templating.Template(TEMPLATE_DIR))
app.attach(pub_router)
app.attach(sec_router)

if __name__ == "__main__":
    app.run()
