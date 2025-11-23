from oxapy import Redirect
from settings import DB


def protect_page(request, next, **kwargs):
    session = request.session()
    is_auth = session.get("is_auth")
    user_id = session.get("user_id")
    if is_auth:
        request.user_id = user_id
        return next(request, **kwargs)
    return Redirect("/login")


def db_session(request, next, **kwargs):
    db = DB()
    try:
        request.db = db
        return next(request, **kwargs)
    finally:
        db.close()
