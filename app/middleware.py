import time
import typing


from config import DB
from oxapy import Redirect, Request, Response


def protect_page(request: Request, next, **kwargs):
    session = request.session
    is_auth = session.get("is_auth")
    user_id = session.get("user_id")
    if is_auth:
        request.user_id = user_id
        return next(request, **kwargs)
    return Redirect("/login")


def db_session(request: Request, next, **kwargs):
    db = DB()
    try:
        request.db = db
        return next(request, **kwargs)
    finally:
        db.close()
