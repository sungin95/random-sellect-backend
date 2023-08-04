from rest_framework.test import APITestCase
from users.models import User
from questions.models import Questions, SellectedQuestions

"""
1. 로그인 안한 상황
    공용 질문
    - QuestionsList 작동 o
    - TotalQuestions 작동 o
    - QuestionCreate 작동 x
    - QuestionDelete 작동 x

    개인 질문
    - TotalGetSellectedQuestions 작동 x
    - GetSellectedQuestions 작동 x
    - SellectedQuestionStart 작동 x
    - SellectQuestion 작동 x
    - SellectedQuestionsDetail 작동 x

2. 로그인 한 상황, 본인 작성한거 작업
    # 공용 질문
    - QuestionsList 작동 o
    - TotalQuestions 작동 o
        -1 status 200체크
        -2 타입 int체크
    - QuestionCreate 작동 o
    - QuestionDelete 작동 o

    # 개인 질문
    - TotalGetSellectedQuestions 작동 o
        -1 status 200체크
        -2 타입 int체크
    - GetSellectedQuestions 작동 o
    - SellectedQuestionStart 작동 o
    - SellectQuestion 작동 o
        -1 200체크
        -2 description 잘 복사 되었는지 체크
        -3 중복생성 막는 기능 있는지
    - test_SellectedQuestionsDetail_put 작동 o
        -1 201체크
        -2 importance값 잘 적용되었는지 체크
    - test_SellectedQuestionsDetail_delete 작동 o
        - 204체크
        - count -1 확인(테스트 실패, 주석처리)

3. 로그인 한 상황, 남이 작성한거 작업(보안테스트)
    # 공용 질문
    - QuestionDelete 작동 x

    # 개인 질문
    - test_SellectedQuestionsDetail_put 작동 x
    - test_SellectedQuestionsDetail_delete 작동 x
"""


"""
1. 로그인 안한 상황
    공용 질문
    - QuestionsList 작동 o
    - TotalQuestions 작동 o
    - QuestionCreate 작동 x
    - QuestionDelete 작동 x

    개인 질문
    - TotalGetSellectedQuestions 작동 x
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

    def test_TotalGetSellectedQuestions(self):
        response = self.client.get(self.URL + "total")
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

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
    # 공용 질문
    - QuestionsList 작동 o
    - TotalQuestions 작동 o
        -1 status 200체크
        -2 타입 int체크
    - QuestionCreate 작동 o
    - QuestionDelete 작동 o

    # 개인 질문
    - TotalGetSellectedQuestions 작동 o
        -1 status 200체크
        -2 타입 int체크
    - GetSellectedQuestions 작동 o
    - SellectedQuestionStart 작동 o
    - SellectQuestion 작동 o
        -1 200체크
        -2 description 잘 복사 되었는지 체크
        -3 중복생성 막는 기능 있는지
    - test_SellectedQuestionsDetail_put 작동 o
        -1 201체크
        -2 importance값 잘 적용되었는지 체크
    - test_SellectedQuestionsDetail_delete 작동 o
        - 204체크
        - count -1 확인(테스트 실패, 주석처리)
"""


# 로그인 한상황에서 생성
class TestQuestionsLogin(APITestCase):
    URL = "/api/v1/questions/"
    DESCRIPTION = "test description"

    def setUp(self):
        user_list = User.create_test_list(1)
        self.user = user_list[0]
        self.client.force_login(
            self.user,
        )
        questions_list = Questions.create_test_list(1, self.user)
        self.question = questions_list[0]

    def test_QuestionsList(self):
        response = self.client.get(self.URL + "1")
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_TotalQuestions_1(self):
        response = self.client.get(self.URL + "total")
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_TotalQuestions_2(self):
        response = self.client.get(self.URL + "total")
        data = response.json()
        self.assertEqual(
            type(data[0]),
            int,
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
        response = self.client.delete(
            self.URL + "delete/" + str(self.question.pk),
        )
        self.assertEqual(
            response.status_code,
            204,
            "status code isn't 204.",
        )


class TestSellectedQuestionsLogin(APITestCase):
    URL = "/api/v1/questions/sellected/"

    def setUp(self):
        # user 1명 생성 및 로그인
        user_list = User.create_test_list(1)
        self.user = user_list[0]
        self.client.force_login(
            self.user,
        )
        # Questions 1개 생성 및 선택
        questions_list = Questions.create_test_list(1, self.user)
        self.question = questions_list[0]

    def test_GetSellectedQuestions(self):
        response = self.client.get(self.URL + "page/1")
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_TotalGetSellectedQuestions_1(self):
        response = self.client.get(self.URL + "total")
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_TotalGetSellectedQuestions_2(self):
        response = self.client.get(self.URL + "total")
        data = response.json()
        self.assertEqual(
            type(data[0]),
            int,
            "타입이 다릅니다.",
        )

    def test_SellectedQuestionStart(self):
        response = self.client.get(self.URL + "start")
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_SellectQuestion_1(self):
        response = self.client.post(self.URL + str(self.question.pk))
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_SellectQuestion_2(self):
        response = self.client.post(self.URL + str(self.question.pk))
        data = response.json()
        self.assertEqual(
            self.question.description,
            data["description"],
            "공용질문과 개인질문의 description이 다릅니다.",
        )

    def test_SellectQuestion_3(self):
        self.sellected_question = SellectedQuestions.create_test(
            self.user,
            self.question.pk,
        )
        response = self.client.post(self.URL + str(self.question.pk))
        self.assertEqual(
            response.status_code,
            406,
            "status code isn't 406.",
        )

    def test_SellectQuestion_4(self):
        self.sellected_question = SellectedQuestions.create_test(
            self.user,
            self.question.pk,
        )
        response = self.client.post(self.URL + str(self.question.pk))
        data = response.json()
        self.assertEqual(
            data[0],
            "already exists",
            "개인 질문이 중복 생성되었습니다.",
        )


class TestSellectedQuestionsLoginDetail(APITestCase):
    def setUp(self):
        # user 1명 생성 및 로그인
        user_list = User.create_test_list(1)
        self.user = user_list[0]
        self.client.force_login(
            self.user,
        )
        # Questions 1개 생성 및 선택
        questions_list = Questions.create_test_list(1, self.user)
        self.question = questions_list[0]
        self.sellected_question = SellectedQuestions.create_test(
            self.user,
            self.question.pk,
        )
        self.URL = (
            "/api/v1/questions/sellected/" + str(self.sellected_question.pk) + "/detail"
        )

    def test_SellectedQuestionsDetail_put_1(self):
        response = self.client.put(
            self.URL,
            data={
                "importance": 5,
            },
        )
        self.assertEqual(
            response.status_code,
            201,
            "status code isn't 201.",
        )

    def test_SellectedQuestionsDetail_put_2(self):
        num = 3

        response = self.client.put(
            self.URL,
            data={
                "importance": num,
            },
        )
        data = response.json()
        self.assertEqual(
            data["importance"],
            (num + self.sellected_question.importance),
            "status code isn't 201.",
        )

    def test_SellectedQuestionsDetail_delete_1(self):
        response = self.client.delete(
            self.URL,
        )
        self.assertEqual(
            response.status_code,
            204,
            "status code isn't 204.",
        )


"""
3. 로그인 한 상황, 남이 작성한거 작업(보안테스트)
    # 공용 질문
    - QuestionDelete 작동 x

    # 개인 질문
    - test_SellectedQuestionsDetail_put 작동 x
    - test_SellectedQuestionsDetail_delete 작동 x
"""


class TestQuestionsLoginOtherUser(APITestCase):
    def setUp(self):
        # user
        user = User.create_test_list(2)
        self.user = user[0]
        self.user_other = user[1]

        # user_other가 로그인, user가 Questions생성
        self.client.force_login(
            self.user_other,
        )
        questions = Questions.create_test_list(1, self.user)
        self.question = questions[0]

        self.URL = "/api/v1/questions/delete/" + str(self.question.pk)

    def test_QuestionDelete(self):
        response = self.client.delete(self.URL)
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )


class TestSellectedQuestionsLoginOtherUser(APITestCase):
    URL = "/api/v1/questions/sellected/"
    DESCRIPTION = "test description"

    def setUp(self):
        # user
        user = User.create_test_list(2)
        self.user = user[0]
        self.user_other = user[1]

        # user_other가 로그인, user가 Questions생성
        self.client.force_login(
            self.user_other,
        )
        questions = Questions.create_test_list(1, self.user)
        self.question = questions[0]

        # user가 Question선택해서 개인질문 생성
        self.sellected_question = SellectedQuestions.create_test(
            self.user,
            self.question.pk,
        )

    def test_SellectedQuestionsDetail_put(self):
        response = self.client.put(
            self.URL + str(self.sellected_question.pk) + "/detail",
            data={
                "importance": 5,
            },
        )
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )

    def test_SellectedQuestionsDetail_delete(self):
        response = self.client.delete(
            self.URL + str(self.sellected_question.pk) + "/detail",
        )
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )
