from oxapy import Router, get, post, put, delete

from core.middleware import protect_page, db_session
from blog.views import (
    about,
    article_form,
    card,
    create_article,
    delete_article,
    edit_form_article,
    get_article,
    home,
    nav,
    update_article,
)

router = (
    Router()
    .routes(
        [
            get("/", home),
            get("/articles/{id:int}", get_article),
            get("/components/article-card/{id:int}", card),
            get("/components/nav", nav),
            get("/about", about),
        ]
    )
    .middleware(db_session)
    .routes(
        [
            delete("/articles/{id:int}", delete_article),
            get("/articles", article_form),
            get("/articles/{id:int}/edit", edit_form_article),
            post("/articles", create_article),
            put("/articles/{id:int}", update_article),
        ]
    )
    .middleware(db_session)
    .middleware(protect_page)
)
