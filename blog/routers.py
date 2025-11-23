from oxapy import Router, get, post, put, delete

from core.middleware import protect_page, db_session
from blog.views import *

router = (
    Router()
    .route(get("/", home))
    .route(get("/articles/{id:int}", get_article))
    .route(get("/components/article-card/{id:int}", card))
    .route(get("/components/nav", nav))
    .middleware(db_session)
    .route(delete("/articles/{id:int}", delete_article))
    .route(get("/articles", article_form))
    .route(get("/articles/{id:int}/edit", edit_form_article))
    .route(post("/articles", create_article))
    .route(put("/articles/{id:int}", update_article))
    .middleware(db_session)
    .middleware(protect_page)
)
