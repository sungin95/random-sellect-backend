from rest_framework.test import APITestCase

from users.models import User


class TestUserSignup(APITestCase):
    URL = "/api/v1/users/signup"

    def test_user_signup_1(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "test1",
                "password": "123",
            },
        )
        self.assertEqual(
            response.status_code,
            201,
            "status code isn't 201.",
        )

    def test_user_signup_2(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "test1",
                "password": "123",
            },
        )
        data = response.json()
        self.assertEqual(
            data["username"],
            "test1",
            "username이 잘못 출력되었습니다.",
        )


class TestUserLogin(APITestCase):
    URL = "/api/v1/users/login"

    def setUp(self):
        user = User.create_test_list(1)[0]
        self.user = user
        self.user_name = "testuser0"
        self.user_pw = "123"

    def test_user_login_1(self):
        response = self.client.post(
            self.URL,
            data={
                "username": self.user_name,
                "password": self.user_pw,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_user_login_2(self):
        response = self.client.post(
            self.URL,
            data={
                "username": self.user_name,
                "password": self.user_pw,
            },
        )
        data = response.json()
        self.assertEqual(
            data,
            {"ok": f"{self.user_name}님 환영합니다. "},
            "로그인 성공시 메시지가 잘못되었습니다.",
        )

    def test_user_login_3(self):
        response = self.client.post(
            self.URL,
            data={
                "username": self.user_name + "_bed",
                "password": self.user_pw,
            },
        )
        self.assertEqual(
            response.status_code,
            400,
            "status code isn't 400.",
        )

    def test_user_login_4(self):
        response = self.client.post(
            self.URL,
            data={
                "username": self.user_name,
                "password": self.user_pw + "123",
            },
        )
        self.assertEqual(
            response.status_code,
            400,
            "status code isn't 400.",
        )

    def test_user_login_5(self):
        response = self.client.post(
            self.URL,
            data={
                "password": self.user_pw,
            },
        )
        self.assertEqual(
            response.status_code,
            400,
            "status code isn't 400.",
        )

    def test_user_login_6(self):
        response = self.client.post(
            self.URL,
            data={
                "username": self.user_name,
            },
        )
        self.assertEqual(
            response.status_code,
            400,
            "status code isn't 400.",
        )

    def test_user_login_7(self):
        response = self.client.post(
            self.URL,
            data={
                "username": self.user_name,
                "password": self.user_pw + "123",
            },
        )
        data = response.json()
        self.assertEqual(
            data,
            {"errors": "아이디 혹은 비밀번호가 잘못되었습니다."},
            "errors 메시지가 잘못되었습니다.",
        )


class TestUserLogout(APITestCase):
    URL = "/api/v1/users/logout"

    def setUp(self):
        user = User.create_test_list(1)[0]
        self.user = user
        self.client.force_login(
            user,
        )

    def test_user_logout_1(self):
        response = self.client.post(
            self.URL,
        )
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )


class TestUserInformation(APITestCase):
    URL = "/api/v1/users/me"

    def setUp(self):
        user = User.create_test_list(1)[0]
        self.user = user

    def test_user_me_get_logout_1(self):
        response = self.client.get(
            self.URL,
        )
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    def test_user_me_get_login_1(self):
        self.client.force_login(
            self.user,
        )
        response = self.client.get(
            self.URL,
        )
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )
