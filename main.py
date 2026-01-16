from oxapy import HttpServer, SessionStore, Router, templating, static_file
from app.views import *
from app.middleware import db_session, protect_page
from config import TEMPLATE_DIR


def main():
    (
        HttpServer(("0.0.0.0", 8000))
        .session_store(SessionStore())
        .template(templating.Template(TEMPLATE_DIR))
        .catchers([not_found_page])
        .attach(Router().route(static_file()))
        .attach(
            Router()
            .middleware(db_session)
            .routes(
                [
                    about,
                    authenticate_user,
                    card,
                    get_article,
                    home,
                    login_form,
                    nav,
                ]
            )
            .scope()
            .middleware(db_session)
            .middleware(protect_page)
            .routes(
                [
                    article_form,
                    create_article,
                    delete_article,
                    edit_form_article,
                    logout,
                    update_article,
                ]
            )
        )
        .run()
    )


if __name__ == "__main__":
    main()
