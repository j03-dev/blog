from functools import wraps
from typing import Any, Callable, TypeVar, List
from oxapy import Request
from sqlalchemy.orm import Session
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from settings import MAIL_TRAP_TOKEN

import smtplib

F = TypeVar("F", bound=Callable[..., Any])


def with_session(func: F) -> F:
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        with Session(request.app_data.engine) as session:  # type: ignore
            return func(request, session, *args, **kwargs)

    return wrapper  # type: ignore


def send_email(recipient_emails: List[str], subject: str, body: str):
    with smtplib.SMTP("live.smtp.mailtrap.io", 587) as server:
        server.starttls()
        server.login("api", MAIL_TRAP_TOKEN)  # type: ignore

        for recipient in recipient_emails:
            msg = MIMEMultipart()
            msg["From"] = "joe@demomailtrap.co"  # type: ignore
            msg["To"] = recipient
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))
            server.send_message(msg)
