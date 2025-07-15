from oxapy import serializer
from core.models import Article


class UserSerializer(serializer.Serializer):
    id = serializer.CharField(read_only=True)
    name = serializer.CharField()
    email = serializer.EmailField()
    password = serializer.CharField(min_length=8, write_only=True, nullable=True)


class ImageSerializer(serializer.Serializer):
    id = serializer.IntegerField()
    path = serializer.CharField()


class ArticleSerializer(serializer.Serializer):
    id = serializer.CharField(read_only=True, required=False, nullable=True)
    title = serializer.CharField()
    content = serializer.CharField()
    author_relationship = UserSerializer(read_only=True, required=False, nullable=True)  # type: ignore

    class Meta:
        model = Article

    def create(self, session, validated_data):
        request = self.context.get("request")
        validated_data = super().validate(validated_data)
        validated_data["author"] = request.user_id
        instance = super().create(session, validated_data)
        return instance


class CredentialSerializer(serializer.Serializer):
    email = serializer.EmailField()
    password = serializer.CharField()
