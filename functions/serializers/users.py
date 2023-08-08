from users.serializers import (
    UserSerializer,
    UserCheckSerializer,
)
from rest_framework.exceptions import ParseError
from users.models import User
from django.db import transaction


def serializer_get_user(user: User):
    serializer = UserSerializer(user)
    return serializer


def serializer_create_user(data, password):
    serializer = UserSerializer(
        data=data,
    )
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(password)
        user.save()
        return {
            "data": serializer.data,
            "model": user,
        }
    return {
        "errors": serializer.errors,
    }


def serializer_put_user(request):
    serializer = UserSerializer(
        request.user,
        data=request.data,
        partial=True,
    )
    if serializer.is_valid():
        serializer.save()
        return {"data": serializer.data}
    return {"errors": serializer}
