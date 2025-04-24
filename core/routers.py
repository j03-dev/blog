from oxapy import Router
from oxapy import static_file

from core import views

pub_router = Router()
pub_router.routes(
    [
        views.index,
        static_file("./static", "static"),
    ]
)
