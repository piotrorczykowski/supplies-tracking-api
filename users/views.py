from typing import override

from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework import viewsets

from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet[User]):
    @override
    def get_serializer_class(self) -> type[UserSerializer]:
        return UserSerializer

    @override
    def get_queryset(self) -> QuerySet[User]:
        return User.objects.all()
