from typing import TypedDict, override

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserValidatedData(TypedDict, total=False):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str


class UserSerializer(serializers.ModelSerializer[User]):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="This email is already in use"
            )
        ],
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True, "required": False}}

    @override
    def create(self, validated_data: UserValidatedData) -> User:
        username = validated_data.get("username")
        password = validated_data.get("password")

        if not username or not password:
            raise ValueError("Missing username or password")

        user = User.objects.create_user(
            username=username,
            email=validated_data.get("email", ""),
            password=password,
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user

    @override
    def update(self, instance: User, validated_data: UserValidatedData) -> User:
        password = validated_data.pop("password", None)

        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        return instance
