from oxapy import HttpServer, SessionStore, Router, templating, static_file

from settings import TEMPLATE_DIR

import app


def main():
    (
        HttpServer(("0.0.0.0", 8000))
        .session_store(SessionStore())
        .template(templating.Template(TEMPLATE_DIR))
        .attach(Router().route(static_file()))
        .attach(app.router)
        .run()
    )


if __name__ == "__main__":
    main()
