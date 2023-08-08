# authenticate: username과 password가 맞으면 user리턴
# login 은 토큰등 필요한것을 자동으로 생성해줌.
# import jwt
# import requests
# from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
from .models import User
from .serializers import UserSerializer
from functions.serializers.users import (
    serializer_get_user,
    serializer_put_user,
    serializer_create_user,
)
from functions.functions import errors_check


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializer_get_user(request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # 현재 안쓰고 있어서 주석처리
    # def put(self, request):
    #     serializer = serializer_put_user(request)
    #     if serializer.get("errors") is None:
    #         return Response(
    #             serializer["data"],
    #             status=status.HTTP_201_CREATED,
    #         )
    #     else:
    #         return Response(
    #             serializer["errors"],
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )


class UserCreate(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = serializer_create_user(request.data, password)
        if errors_check(serializer):
            login(request, serializer["model"])
            return Response(
                serializer["data"],
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"errors"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            # login시키고 백엔드에 세션 생성, 사용자에게 cookie제공
            login(request, user)
            return Response(
                {"ok": f"{user.username}님 환영합니다. "},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"errors": "아이디 혹은 비밀번호가 잘못되었습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            {"ok": "bye!"},
            status=status.HTTP_200_OK,
        )


# 화면이 준비 안되서 안쓰는 중
# class ChangePassword(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request):
#         user = request.user
#         old_password = request.data.get("old_password")
#         new_password = request.data.get("new_password")
#         if not old_password or not new_password:
#             raise ParseError
#         if user.check_password(old_password):
#             user.set_password(new_password)
#             user.save()
#             return Response(status=status.HTTP_200_OK)
#         else:
#             raise ParseError
