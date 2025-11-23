from oxapy import serializer


class UserSerializer(serializer.Serializer):
    id = serializer.CharField(read_only=True)
    name = serializer.CharField()
    email = serializer.EmailField()
    password = serializer.CharField(min_length=8, write_only=True, nullable=True)


class CredentialSerializer(serializer.Serializer):
    email = serializer.EmailField()
    password = serializer.CharField()
