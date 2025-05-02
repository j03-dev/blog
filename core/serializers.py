from oxapy import serializer


class UserInputSerialier(serializer.Serializer):
    name = serializer.CharField()
    email = serializer.EmailField()
    password = serializer.CharField(
        min_length=8, description="minimum length is 8")


class UserModelSerializer(serializer.Serializer):
    id = serializer.CharField()
    name = serializer.CharField()
    email = serializer.CharField()


class ImageModelSerializer(serializer.Serializer):
    id = serializer.IntegerField()
    path = serializer.CharField()


class ArticleInputSerializer(serializer.Serializer):
    title = serializer.CharField()
    content = serializer.CharField()


class ArticleModelSerializer(serializer.Serializer):
    id = serializer.IntegerField()
    title = serializer.CharField()
    content = serializer.CharField()
    at = serializer.DateTimeField()

    def to_representation(self, instance):
        data = super().to_representation(instance)

        additional = {
            "author": UserModelSerializer(instance=instance.author_relationship).data,
            "images": ImageModelSerializer(instance=instance.images, many=True).data,
            "at": data["at"].strftime("%d %B %Y")
        }

        data.update(additional)

        return data


class CredentialSerializer(serializer.Serializer):
    email = serializer.EmailField()
    password = serializer.CharField()
