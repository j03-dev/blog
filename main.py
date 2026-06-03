from oxapy import HttpServer, Session, Router, templating, static_file
from app import views
from app.middleware import db_session, protect_page
from config import TEMPLATE_DIR, SECRET


def main():
    session = Session(bytes(SECRET, encoding="utf-8"))  # type: ignore
    (
        HttpServer(("0.0.0.0", 8000))
        .template(templating.Template(TEMPLATE_DIR))
        .catchers([views.not_found_page])
        .attach(Router().route(static_file()))
        .attach(
            Router()
            .middleware(session)
            .middleware(db_session)
            .routes(
                [
                    views.about,
                    views.authenticate_user,
                    views.get_article,
                    views.home,
                    views.login_form,
                ]
            )
            .scope()
            .middleware(session)
            .middleware(db_session)
            .middleware(protect_page)
            .routes(
                [
                    views.article_form,
                    views.create_article,
                    views.delete_article,
                    views.edit_form_article,
                    views.logout,
                    views.update_article,
                ]
            )
        )
        .run()
    )


if __name__ == "__main__":
    main()
