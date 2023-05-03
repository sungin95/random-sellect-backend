from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework import status
from questions.models import Questions
from sellectedQuestions.models import SellectedQuestion
from sellectedQuestions.serializers import (
    SellectedQuestionSerializer,
    ShowSellectedQuestionSerializer,
    ImportanceSellectedQuestionSerializer,
)
from django.db import transaction
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from questions.serializers import QuestionsCreateSerializer
import random


# 내 질문 목록 보기(get)
class SellectedQuestions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions = SellectedQuestion.objects.filter(user=request.user)
        serializer = ShowSellectedQuestionSerializer(questions, many=True)
        return Response(serializer.data)


class SellectedQuestionStart(APIView):
    permission_classes = [IsAuthenticated]

    def start(self, request):
        sum_list = []
        sum_ = 0
        for i in SellectedQuestion.objects.filter(user=request.user):
            sum_ += i.importance
            for j in range(i.importance):
                sum_list.append(i)
        try:
            return random.choice(sum_list)
        except:
            # 오류를 대비해 값을 넣어 두었음.
            return {
                "pk": 0,
                "description": "질문지가 없습니다.",
                "importance": 3,
            }

    def get(self, request):
        sellectedquestion = self.start(request)
        serializer = ShowSellectedQuestionSerializer(sellectedquestion)
        return Response(serializer.data)


# 생성(post),
class SellectQuestion(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Questions.objects.get(pk=pk)
        except Questions.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        question = self.get_object(pk)
        questions = SellectedQuestion.objects.filter(
            question=question, user=request.user
        )
        if len(questions) == 0:
            sellectedQuestionSerializer = SellectedQuestionSerializer(
                data=QuestionsCreateSerializer(question).data
            )
            if sellectedQuestionSerializer.is_valid():
                sellectedQuestionSerializer.save(
                    question=question,
                    user=request.user,
                )
                question.count += 1
                question.save()

                return Response(
                    {
                        "ok": "ok",
                    },
                )
            else:
                return Response(
                    sellectedQuestionSerializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"already exists"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )


# 수정(put, importance), 삭제(delete)
class SellectedQuestionsDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return SellectedQuestion.objects.get(pk=pk)
        except SellectedQuestion.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        sellectedQuestion = self.get_object(pk)
        # 검증
        if sellectedQuestion.user != request.user:
            raise PermissionDenied

        serializer = ImportanceSellectedQuestionSerializer(
            sellectedQuestion,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_importance = serializer.save()
            return Response(
                ImportanceSellectedQuestionSerializer(updated_importance).data
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        sellectedQuestion = self.get_object(pk)
        # 검증
        if sellectedQuestion.user != request.user:
            raise PermissionDenied

        q = sellectedQuestion.question
        q.count -= 1
        q.save()
        sellectedQuestion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
