from oxapy import HttpServer, SessionStore, Router, templating, static_file

from authentication.routers import router as auth_router
from blog.routers import router as blog_router

from settings import TEMPLATE_DIR


def main():
    (
        HttpServer(("0.0.0.0", 8000))
        .session_store(SessionStore())
        .template(templating.Template(TEMPLATE_DIR))
        .attach(Router().route(static_file()))
        .attach(auth_router)
        .attach(blog_router)
        .run()
    )


if __name__ == "__main__":
    main()
