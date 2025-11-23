from sqlalchemy.orm import Session
from authentication import repositories as repo
from authentication.serializers import CredentialSerializer


def login(session: Session, cred: CredentialSerializer):
    if user := repo.get_user_by_email(session, cred.validated_data["email"]):
        if user.password == cred.validated_data["password"]:
            return user
    return None
