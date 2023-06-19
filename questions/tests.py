from rest_framework.test import APITestCase
from users.models import User
from .models import *

"""
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
        response = self.client.post(self.URL + "create")
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    def test_QuestionDelete(self):
        response = self.client.delete(self.URL + "delete/1")
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
        response = self.client.post(self.URL + "1")
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    def test_SellectedQuestionsDetail_put(self):
        response = self.client.put(self.URL + "1/detail")
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    def test_SellectedQuestionsDetail_delete(self):
        response = self.client.delete(self.URL + "1/detail")
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )


"""
2. 로그인 한 상황, 본인 작성한거 작업
    - QuestionsList 작동 o
    - TotalQuestions 작동 o
    - QuestionCreate 작동 o
    - QuestionDelete 작동 o

    - TotalGetSellectedQuestions 작동 o
    - GetSellectedQuestions 작동 o
    - SellectedQuestionStart 작동 o
    - SellectQuestion 작동 o
    - SellectedQuestionsDetail 작동 o
"""


# 로그인 한상황에서 생성
class TestQuestionsLogin(APITestCase):
    URL = "/api/v1/questions/"
    DESCRIPTION = "test description"

    def setUp(self):
        user = User.objects.create(
            username="testuser",
        )
        user.set_password("123")
        user.save()
        self.user = user
        self.client.force_login(
            self.user,
        )
        self.question = Questions.objects.create(
            description=self.DESCRIPTION,
            authon=self.user,
        )

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
        response = self.client.post(
            self.URL + "create",
            data={
                "description": self.DESCRIPTION,
            },
        )
        data = response.json()
        self.assertEqual(
            data["description"],
            self.DESCRIPTION,
            "description이 제대로 전달이 안되었습니다. ",
        )
        self.assertEqual(
            response.status_code,
            201,
            "status code isn't 201.",
        )

    def test_QuestionDelete(self):
        response = self.client.delete(self.URL + "delete/" + str(self.question.pk))
        # data = response.json() # ! 이거 때문에 에러... 주의!!!
        self.assertEqual(
            response.status_code,
            204,
            "status code isn't 204.",
        )


class TestSellectedQuestionsLogin(APITestCase):
    URL = "/api/v1/questions/sellected/"
    DESCRIPTION = "test description"

    def setUp(self):
        user = User.objects.create(
            username="testuser",
        )
        user.set_password("123")
        user.save()
        self.user = user
        self.client.force_login(
            self.user,
        )
        self.question = Questions.objects.create(
            description=self.DESCRIPTION,
            authon=self.user,
        )

    def test_GetSellectedQuestions(self):
        response = self.client.get(self.URL + "page/1")
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_TotalGetSellectedQuestions(self):
        response = self.client.get(self.URL + "total")
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_SellectedQuestionStart(self):
        response = self.client.get(self.URL + "start")
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_SellectQuestion(self):
        # print(str(self.question.pk))
        response = self.client.post(self.URL + "1")
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    # def test_SellectedQuestionsDetail_put(self):
    #     response = self.client.put(self.URL + "1/detail")
    #     self.assertEqual(
    #         response.status_code,
    #         403,
    #         "status code isn't 403.",
    #     )

    # def test_SellectedQuestionsDetail_delete(self):
    #     response = self.client.delete(self.URL + "1/detail")
    #     self.assertEqual(
    #         response.status_code,
    #         403,
    #         "status code isn't 403.",
    #     )
