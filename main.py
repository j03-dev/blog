from oxapy import HttpServer, Session, Router, templating, static_file
from app.views import *
from app.middleware import db_session, protect_page
from config import TEMPLATE_DIR, SECRET


def main():
    session = Session(bytes(SECRET, encoding="utf-8"))  # type: ignore
    (
        HttpServer(("0.0.0.0", 8000))
        .template(templating.Template(TEMPLATE_DIR))
        .catchers([not_found_page])
        .attach(Router().route(static_file()))
        .attach(
            Router()
            .middleware(session)
            .middleware(db_session)
            .routes(
                [
                    about,
                    authenticate_user,
                    get_article,
                    home,
                    login_form,
                    nav,
                ]
            )
            .scope()
            .middleware(session)
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
