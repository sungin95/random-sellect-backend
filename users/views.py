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


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UserCreate(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = UserSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = UserSerializer(user)
            login(request, user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            return Response({"ok": "Welcome!"})
        else:
            return Response(
                {"error": "wrong password"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


# class JWTLogIn(APIView):
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         if not username or not password:
#             raise ParseError
#         user = authenticate(
#             request,
#             username=username,
#             password=password,
#         )
#         if user:
#             # secret_key가 중요하다.
#             token = jwt.encode(
#                 {"pk": user.pk},
#                 settings.SECRET_KEY,
#                 algorithm="HS256",
#             )
#             return Response({"token": token})
#         else:
#             return Response({"error": "wrong password"})


# class GithubLogin(APIView):
#     def post(self, request):
#         try:
#             code = request.data.get("code")
#             access_token = requests.post(
#                 f"https://github.com/login/oauth/access_token?code={code}&client_id=c6102a1014c5e26e2c21&client_secret={settings.GH_SECRET}",
#                 headers={"Accept": "application/json"},
#             )
#             access_token = access_token.json().get("access_token")
#             user_data = requests.get(
#                 "https://api.github.com/user",
#                 headers={
#                     "Authorization": f"Bearer {access_token}",
#                     "Accept": "application/json",
#                 },
#             )
#             user_data = user_data.json()
#             # user email
#             user_emails = requests.get(
#                 "https://api.github.com/user/emails",
#                 headers={
#                     "Authorization": f"Bearer {access_token}",
#                     "Accept": "application/json",
#                 },
#             )
#             user_emails = user_emails.json()
#             try:
#                 user = User.objects.get(email=user_emails[0]["email"])
#                 login(request, user)
#                 return Response(status=status.HTTP_200_OK)
#             except User.DoesNotExist:
#                 user = User.objects.create(
#                     username=user_data.get("login"),
#                     email=user_emails[0]["email"],
#                     name=user_data.get("name"),
#                     avatar=user_data.get("avatar_url"),
#                 )
#                 # 장고 4.1 ref/contrib/auth
#                 user.set_unusable_password()
#                 user.save()
#                 login(request, user)
#                 return Response(status=status.HTTP_200_OK)
#         except Exception:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


# class KakaoLogIn(APIView):
#     def post(self, request):
#         try:
#             code = request.data.get("code")
#             access_token = requests.post(
#                 "https://kauth.kakao.com/oauth/token",
#                 headers={"Content-Type": "application/x-www-form-urlencoded"},
#                 data={
#                     "grant_type": "authorization_code",
#                     "client_id": "0999329903a4ff2d986c09fdd71eb44f",
#                     "redirect_uri": "http://127.0.0.1:3000/social/kakao",
#                     "code": code,
#                 },
#             )
#             access_token = access_token.json().get("access_token")
#             user_data = requests.get(
#                 "https://kapi.kakao.com/v2/user/me",
#                 headers={
#                     "Authorization": f"Bearer {access_token}",
#                     "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
#                 },
#             )
#             user_data = user_data.json()
#             kakao_account = user_data.get("kakao_account")
#             profile = kakao_account.get("profile")
#             try:
#                 user = User.objects.get(email=kakao_account.get("email"))
#                 login(request, user)
#                 return Response(status=status.HTTP_200_OK)
#             except User.DoesNotExist:
#                 user = User.objects.create(
#                     email=kakao_account.get("email"),
#                     username=profile.get("nickname"),
#                     name=profile.get("nickname"),
#                     avatar=profile.get("profile_image_url"),
#                 )
#                 user.set_unusable_password()
#                 user.save()
#                 login(request, user)
#                 return Response(status=status.HTTP_200_OK)
#         except Exception:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
