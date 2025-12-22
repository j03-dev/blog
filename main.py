from oxapy import HttpServer, SessionStore, Router, templating, static_file
from app.views import *
from app.middleware import db_session, protect_page
from config import TEMPLATE_DIR


def main():
    (
        HttpServer(("0.0.0.0", 8000))
        .session_store(SessionStore())
        .template(templating.Template(TEMPLATE_DIR))
        .attach(Router().route(static_file()))
        .attach(
            Router()
            .middleware(db_session)
            .routes([home, login_form, authenticate_user, nav, card, about, get_article])
            .scope()
            .middleware(db_session)
            .middleware(protect_page)
            .routes(
                [
                    logout,
                    article_form,
                    create_article,
                    edit_form_article,
                    update_article,
                    delete_article,
                ]
            )
        )
        .run()
    )


if __name__ == "__main__":
    main()
