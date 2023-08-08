from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    PermissionDenied,
    ParseError,
)  # NotFound,NotAuthenticated,ParseError,
from rest_framework import status
from .models import Questions, SellectedQuestions
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from config import settings
import random

from functions.functions import page_nation, user_not_equal
from functions.errors import errors_check
from functions.serializers.createQ_QS import (
    serializer_create_Question_sellectedQuestion,
)
from functions.serializers.questions import serializer_get_questions
from functions.serializers.sellectedQuestions import (
    serializer_get_sellectedQuestion,
    serializer_get_sellectedQuestions,
    serializer_create_sellectedQuestion,
    serializer_put_sellectedQuestion_importance,
)


class TotalQuestions(APIView):
    def get(self, request):
        total_questions = Questions.objects.all().count()
        list_total_questions = [total_questions]
        return Response(list_total_questions, status.HTTP_200_OK)


class QuestionsList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, page):
        (start, end) = page_nation(settings.PAGE_SIZE, page)
        all_questions = Questions.objects.all().order_by("-count")[start:end]
        serializer = serializer_get_questions(all_questions)
        return Response(serializer.data, status.HTTP_200_OK)


class QuestionCreate(APIView):
    # 질문 만들기, 나의 질문에 추가하기
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializer_create_Question_sellectedQuestion(request)
        if errors_check(serializer):
            return Response(
                serializer["question"],
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer["errors"],
            status=status.HTTP_400_BAD_REQUEST,
        )


# 아직 사용 안하고 있음
class QuestionDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, questions_pk):
        question = Questions.get_object(questions_pk)
        if user_not_equal(request.user, question.authon):
            raise PermissionDenied
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ------------- SellectedQuestions ---------------


class TotalGetSellectedQuestions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_sellected_questions = SellectedQuestions.get_login_user_of_SQ(
            request.user,
        ).count()
        list_total_sellected_questions = [total_sellected_questions]
        return Response(list_total_sellected_questions, status.HTTP_200_OK)


# 내 질문 목록 보기(get)
class GetSellectedQuestions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, page):
        (start, end) = page_nation(settings.PAGE_SIZE, page)
        sellected_questions = SellectedQuestions.get_login_user_of_SQ(
            request.user,
        )[start:end]
        serializer = serializer_get_sellectedQuestions(sellected_questions)
        return Response(serializer.data, status.HTTP_200_OK)


class SellectedQuestionStart(APIView):
    permission_classes = [IsAuthenticated]

    def start(self, request):
        sellected_questions = SellectedQuestions.get_login_user_of_SQ(
            request.user,
        )
        if sellected_questions.exists():
            selection_probability = [
                question.importance for question in sellected_questions
            ]

            selected_question = random.choices(
                sellected_questions, weights=selection_probability
            )[0]

            return selected_question

        else:
            # 오류를 대비해 값을 넣어 두었음.(프론트 구현이 미흡해서 이상하지만 이렇게 넣었습니다. )
            return {
                "pk": 0,
                "description": "질문지가 없습니다.",
                "importance": 3,
            }

    def get(self, request):
        sellectedquestion = self.start(request)
        serializer = serializer_get_sellectedQuestion(
            sellectedquestion,
        )
        return Response(serializer.data, status.HTTP_200_OK)


# 생성(post),
class SellectQuestion(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, question_pk):
        question = Questions.get_object(question_pk)
        # 이미 선택했나 확인 => 없으면(0) 생성, 있으면(!0) 406 에러
        sellected_questions = SellectedQuestions.get_login_user_of_SQ(
            request.user,
        ).filter(
            question=question.pk,
        )

        if not sellected_questions.exists():
            sellectedQuestionSerializer = serializer_create_sellectedQuestion(
                request,
                question,
            )
            if errors_check(sellectedQuestionSerializer):
                return Response(
                    sellectedQuestionSerializer["data"],
                    status=status.HTTP_200_OK,
                )

            return Response(
                sellectedQuestionSerializer["errors"],
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {"already exists"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )


# 수정(importance), 삭제
class SellectedQuestionsDetail(APIView):
    permission_classes = [IsAuthenticated]

    # importance만 처리 되도록 되어있음
    def put(self, request, sq_pk):
        sellectedQuestion = SellectedQuestions.get_object(sq_pk)

        if user_not_equal(request.user, sellectedQuestion.user):
            raise PermissionDenied

        if not request.data["importance"]:
            raise ParseError

        serializer = serializer_put_sellectedQuestion_importance(
            request.data["importance"], sellectedQuestion
        )

        if errors_check(serializer):
            return Response(
                serializer["data"],
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer["errors"],
            status=status.HTTP_400_BAD_REQUEST,
        )

    # delete메소드는 Response에 본문을 추가할 수 없어서 count-1이 되는지 테스트 케이스 작성 X
    def delete(self, request, sq_pk):
        sellectedQuestion = SellectedQuestions.get_object(sq_pk)

        if user_not_equal(request.user, sellectedQuestion.user):
            raise PermissionDenied

        question_pk = sellectedQuestion.question.pk
        sellectedQuestion.delete_count(question_pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
