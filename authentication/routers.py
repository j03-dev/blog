from oxapy import Router, get, post

from core.middleware import protect_page, db_session
from authentication.views import login_page, login, logout

router = (
    Router()
    .route(get("/login", login_page))
    .route(post("/login", login))
    .middleware(db_session)
    .route(get("/logout", logout))
    .middleware(db_session)
    .middleware(protect_page)
)
