from functools import wraps
from typing import Any, Callable, TypeVar, List
from oxapy import Request
from sqlalchemy.orm import Session
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from settings import EMAIL_ADDR, EMAIL_PASSWORD

import smtplib

F = TypeVar("F", bound=Callable[..., Any])


def with_session(func: F) -> F:
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        with Session(request.app_data.engine) as session:  # type: ignore
            return func(request, session, *args, **kwargs)

    return wrapper  # type: ignore


def send_email(recipient_emails: List[str], subject: str, body: str):
    server = smtplib.SMTP("smpt.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_ADDR, EMAIL_PASSWORD)  # type: ignore

    for recipient in recipient_emails:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDR  # type: ignore
        msg["To"] = recipient
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))
        server.send_message(msg)

    server.quit()
