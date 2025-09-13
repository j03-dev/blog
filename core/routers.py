from oxapy import Router, Request, static_file, Redirect

from core import views
from settings import DB

from logging import log


def protect_page(request: Request, next, **kwargs):
    session = request.session()  # type: ignore
    is_auth = session.get("is_auth")
    user_id = session.get("user_id")

    if is_auth:
        request.user_id = user_id
        return next(request, **kwargs)
    return Redirect("/login")


def db_session(request, next, **kwargs):
    db = DB()
    try:
        setattr(request, "db", db)
        return next(request, **kwargs)
    finally:
        db.close()


pub_router = Router()
pub_router.middleware(db_session)
pub_router.routes(
    [
        views.nav,
        views.home,
        views.login,
        views.login_form,
        views.card,
        views.get_article,
        static_file("./static", "static"),
    ]
)

sec_router = Router()
sec_router.middleware(protect_page)
sec_router.middleware(db_session)
sec_router.routes(
    [
        views.article_form,
        views.edit_form_article,
        views.update_article,
        views.create_article,
        views.delete_article,
        views.logout,
    ]
)
