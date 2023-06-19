from rest_framework.test import APITestCase
from users.models import User
from .models import *

"""
함수 - 목적
1. 로그인 안한 상황
    - QuestionsList 작동 o
    - TotalQuestions 작동 o
    - QuestionCreate 작동 x
    - QuestionDelete 작동 x

    - TotalGetSellectedQuestions 작동 x (request.user가 필요해서 실험x)
    - GetSellectedQuestions 작동 x
    - SellectedQuestionStart 작동 x
    - SellectQuestion 작동 x
    - SellectedQuestionsDetail 작동 x
    - delete 작동 x
"""


# 로그인 안한상황에서 생성
class TestQuestionsLogout(APITestCase):
    URL = "/api/v1/questions/"

    def test_QuestionsList(self):
        response = self.client.get(self.URL + "1")
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_TotalQuestions(self):
        response = self.client.get(self.URL + "total")
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_QuestionCreate(self):
        response = self.client.get(self.URL + "create")
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    def test_QuestionDelete(self):
        response = self.client.get(self.URL + "delete/1")
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )


class TestSellectedQuestionsLogout(APITestCase):
    URL = "/api/v1/questions/sellected/"

    def test_GetSellectedQuestions(self):
        response = self.client.get(self.URL + "page/1")
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    # def test_TotalGetSellectedQuestions(self):
    #     response = self.client.get(self.URL + "total")
    #     self.assertEqual(
    #         response.status_code,
    #         403,
    #         "status code isn't 403.",
    #     )

    def test_SellectedQuestionStart(self):
        response = self.client.get(self.URL + "start")
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    def test_SellectQuestion(self):
        response = self.client.get(self.URL + "1")
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    def test_SellectedQuestionsDetail(self):
        response = self.client.get(self.URL + "1/detail")
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )
