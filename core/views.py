from oxapy import get, Request, templating

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from core.models import Article
from core.serializers import ArticleModelSerializer


@get("/")
def index(request: Request):
    with Session(request.app_data.engine) as session:
        stmt = select(Article).options(
            joinedload(Article.author_relationship),
            joinedload(Article.images),
        )
        articles = session.execute(stmt).unique().scalars().all()
        serializer = ArticleModelSerializer(instance=articles, many=True)
        return templating.render(
            request, "index.html.j2", {"articles": serializer.data}
        )
