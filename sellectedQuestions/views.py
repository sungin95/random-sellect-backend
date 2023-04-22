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


# 내 질문 목록 보기(get)
class SellectedQuestions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions = SellectedQuestion.objects.filter(user=request.user)
        serializer = ShowSellectedQuestionSerializer(questions, many=True)
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
        sellectedQuestionSerializer = SellectedQuestionSerializer(
            data=QuestionsCreateSerializer(question).data
        )
        if sellectedQuestionSerializer.is_valid():
            sellectedQuestionSerializer.save(
                question=question,
                user=request.user,
            )
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

        sellectedQuestion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
