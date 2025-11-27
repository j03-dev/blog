from oxapy import Router

from app.views import *

from core.middleware import db_session, protect_page

router = (
    Router()
    .routes([login_form, authenticate_user, nav, card, about, get_article])
    .middleware(db_session)
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
    .middleware(db_session)
    .middleware(protect_page)
)
