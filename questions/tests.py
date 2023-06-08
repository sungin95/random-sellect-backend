from rest_framework.test import APITestCase
from users.models import User
from .models import *


# 로그인 안한상황에서 생성
class TestQuestions(APITestCase):
    URL = "/api/v1/questions/"

    def test_total_count_num(self):
        response = self.client.get(self.URL + "total")
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )
