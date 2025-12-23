from oxapy import serializer

from app.models import Article


class UserSerializer(serializer.Serializer):
    id = serializer.CharField(read_only=True)
    name = serializer.CharField()
    email = serializer.EmailField()
    password = serializer.CharField(min_length=8, write_only=True, nullable=True)


class CredentialSerializer(serializer.Serializer):
    email = serializer.EmailField()
    password = serializer.CharField(min_length=8)


class ImageSerializer(serializer.Serializer):
    id = serializer.IntegerField()
    path = serializer.CharField()


class ArticleSerializer(serializer.Serializer):
    id = serializer.CharField(read_only=True, required=False, nullable=True)
    title = serializer.CharField()
    content = serializer.CharField()
    author_relationship = UserSerializer(read_only=True, required=False, nullable=True)
    at = serializer.DateField(required=False, nullable=True, read_only=True)

    class Meta:
        model = Article

    def validate(self, attr):
        attr = super().validate(attr)
        content: str = attr["content"]
        if len(content.strip()) == 0:
            raise serializer.ValidationException("content should not empty")
        return attr

    def create(self, session, validated_data):
        request = self.context.get("request")
        validated_data = super().validate(validated_data)
        validated_data["author"] = request.user_id
        instance = super().create(session, validated_data)
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["at"] = instance.at.strftime("%B %d, %Y")
        return data
