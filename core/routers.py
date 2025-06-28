from oxapy import Router, Request, static_file, Redirect, Response, convert_to_response

from core import views

import logging


def pref(request: Request, next, **kwargs):
    session = request.session()  # type: ignore
    theme = session.get("theme")
    if not theme:
        theme = "ligth"
        session["theme"] = theme

    response: Response = convert_to_response(next(request, **kwargs))
    response.insert_header("Set-Cookie", f"theme={theme};Path=/")
    return response


def protect_page(request: Request, next, **kwargs):
    session = request.session()  # type: ignore
    is_auth = session.get("is_auth")
    user_id = session.get("user_id")

    if is_auth:
        request.user_id = user_id
        return next(request, **kwargs)
    return Redirect("/login")


def logger(request, next, **kwargs):
    logging.log(1000, f"{request.method} {request.uri}")
    return next(request, **kwargs)


pub_router = Router()
pub_router.middleware(logger)
pub_router.middleware(pref)
pub_router.routes(
    [
        views.nav,
        views.home,
        views.login,
        views.login_form,
        views.articles,
        views.get_article,
        static_file("./static", "static"),
    ]
)

sec_router = Router()
sec_router.middleware(logger)
sec_router.middleware(protect_page)
sec_router.middleware(pref)
sec_router.routes(
    [
        views.article_form,
        views.edit_form_article,
        views.update_article,
        views.create_article,
        views.delete_article,
    ]
)
