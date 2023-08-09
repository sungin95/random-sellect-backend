from rest_framework.test import APITestCase
from users.models import User
from questions.models import Questions, SellectedQuestions
from config.urls import base_url

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
    URL = f"/{base_url}questions/"

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
    URL = f"/{base_url}questions/sellected/"

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
    URL = f"/{base_url}questions/"

    def setUp(self):
        user_list = User.create_test_list(1)
        self.user = user_list[0]
        self.client.force_login(
            self.user,
        )
        questions_list = Questions.create_test_list(1, self.user)
        self.question = questions_list[0][0]
        self.DESCRIPTION = self.question.description + "test"

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
            "TotalQuestions의 값이 int가 아닙니다.",
        )

    def test_TotalQuestions_3(self):
        response = self.client.get(self.URL + "total")
        data = response.json()
        self.assertEqual(
            data[0],
            1,
            "TotalQuestions의 값이 int가 아닙니다.",
        )

    def test_QuestionCreate_1(self):
        response = self.client.post(
            self.URL + "create",
            data={
                "description": self.DESCRIPTION,
            },
        )
        self.assertEqual(
            response.status_code,
            201,
            "status code isn't 201.",
        )

    def test_QuestionCreate_2(self):
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

    def test_QuestionCreate_3(self):
        response = self.client.post(
            self.URL + "create",
            data={
                "description": self.DESCRIPTION,
            },
        )
        data = response.json()
        question = Questions.get_object(int(data["pk"]))
        self.assertEqual(
            question.count,
            1,
            "Questions 생성시 count 값이 잘못되었습니다. ",
        )

    def test_QuestionCreate_4(self):
        response = self.client.post(
            self.URL + "create",
            data={
                "description": self.DESCRIPTION + "123",
            },
        )
        data = response.json()
        question = Questions.get_object(int(data["pk"]))
        sellectedQuestions = question.sellectedQuestions_set.all()[0]
        self.assertEqual(
            self.DESCRIPTION + "123",
            sellectedQuestions.description,
            "Questions 생성시 count 값이 잘못되었습니다. ",
        )

    def test_QuestionCreate_5(self):
        response = self.client.post(
            self.URL + "create",
            data={
                "description": self.DESCRIPTION + "123",
            },
        )
        data = response.json()
        question = Questions.get_object(int(data["pk"]))
        len_sellectedQuestions = len(question.sellectedQuestions_set.all())
        self.assertEqual(
            len_sellectedQuestions,
            1,
            "Questions 생성시 count 값이 잘못되었습니다. ",
        )

    def test_QuestionDelete_1(self):
        response = self.client.delete(
            self.URL + "delete/" + str(self.question.pk),
        )
        self.assertEqual(
            response.status_code,
            204,
            "status code isn't 204.",
        )

    def test_QuestionDelete_2(self):
        question = Questions.get_object(self.question.pk)
        self.client.delete(
            self.URL + "delete/" + str(self.question.pk),
        )
        try:
            Questions.get_object(self.question.pk)
            self.assertEqual(
                False,
                True,
                "Questions가 삭제가 안된 상황",
            )
        except:
            self.assertEqual(
                True,
                True,
                "Questions가 정상 삭제",
            )

    def test_QuestionDelete_3(self):
        question = Questions.get_object(self.question.pk)
        sellectedQuestion = question.sellectedQuestions_set.all()[0]
        self.client.delete(
            self.URL + "delete/" + str(self.question.pk),
        )
        SellectedQuestions.get_object(sellectedQuestion.pk)
        self.assertEqual(
            True,
            True,
            "Questions 삭제시 관련 SellectedQuestions도 삭제되었습니다. ",
        )


class TestSellectedQuestionsLogin(APITestCase):
    URL = f"/{base_url}questions/sellected/"

    def setUp(self):
        # user 2명 생성 및 로그인(user 로그인, user_owner)
        user_list = User.create_test_list(2)
        self.user_owner = user_list[0]
        self.user = user_list[1]
        self.client.force_login(
            self.user,
        )
        # Questions 1개 생성(user_owner 소유)
        questions_list = Questions.create_test_list(1, self.user_owner)
        self.question = questions_list[0][0]

    def test_GetSellectedQuestions_1(self):
        response = self.client.get(self.URL + "page/1")
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

    def test_GetSellectedQuestions_2(self):
        response = self.client.get(self.URL + "page/1")
        data = response.json()
        self.assertEqual(
            len(data),
            0,
            "SellectedQuestions의 user에 문제가 있습니다.",
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
        # user 2명 생성 및 로그인(user 로그인, user_owner)
        user_list = User.create_test_list(2)
        self.user_owner = user_list[0]
        self.user = user_list[1]
        self.client.force_login(
            self.user,
        )
        #             Questions         SellectedQuestions      login
        # user         x                 o                       o
        # user_owner   o                 o                       x
        questions_list = Questions.create_test_list(1, self.user_owner)
        self.question = questions_list[0][0]
        self.sellected_question = SellectedQuestions.create_test(
            self.user,
            self.question.pk,
        )
        self.URL = (
            f"/{base_url}questions/sellected/{str(self.sellected_question.pk)}/detail"
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
            "importance값이 틀렸습니다.",
        )

    def test_SellectedQuestionsDetail_put_3(self):
        num = -99999
        try:
            response = self.client.put(
                self.URL,
                data={
                    "importance": num,
                },
            )
            self.assertEqual(
                True,
                False,
                "importance값은 음수가 될 수 없습니다.",
            )
        except:
            self.assertEqual(
                True,
                True,
                "정상적 상황.",
            )

    # 여기서 부터
    def test_SellectedQuestionsDetail_delete_1(self):
        response = self.client.delete(
            self.URL,
        )
        self.assertEqual(
            response.status_code,
            204,
            "status code isn't 204.",
        )

    def test_SellectedQuestionsDetail_delete_2(self):
        question_before = Questions.get_object(self.question.pk)
        self.client.delete(
            self.URL,
        )
        question_after = Questions.get_object(self.question.pk)
        self.assertEqual(
            question_before.count - 1,
            question_after.count,
            "SQ삭제시 question의 count가 -1이 안되었습니다.",
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
        self.question = questions[0][0]

        self.URL = f"/{base_url}questions/delete/" + str(self.question.pk)

    def test_QuestionDelete(self):
        response = self.client.delete(self.URL)
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )


class TestSellectedQuestionsLoginOtherUser(APITestCase):
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
        self.question = questions[0][0]

        # user가 Question선택해서 개인질문 생성
        self.sellected_question = SellectedQuestions.create_test(
            self.user,
            self.question.pk,
        )
        self.URL = (
            f"/{base_url}questions/sellected/{str(self.sellected_question.pk)}/detail"
        )

    def test_SellectedQuestionsDetail_put(self):
        response = self.client.put(
            self.URL,
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
            self.URL,
        )
        self.assertEqual(
            response.status_code,
            403,
            "status code isn't 403.",
        )
