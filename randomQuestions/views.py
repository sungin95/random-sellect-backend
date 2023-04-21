from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework import status
from .models import Questions, QuestionUser
from .serializers import (
    QuestionsSerializer,
    QuestionUserSerializer,
    QuestionsCreateSerializer,
)
from django.db import transaction


class QuestionsList(APIView):
    def get(self, request):
        all_questions = Questions.objects.all()
        serializer = QuestionsSerializer(all_questions, many=True)
        return Response(serializer.data)

    # 질문 만들기, 나의 질문에 추가하기
    def post(self, request):
        # 질문 만들기
        questionsSerializer = QuestionsCreateSerializer(data=request.data)
        if questionsSerializer.is_valid():
            question = questionsSerializer.save(authon=request.user)
            # 나의 질문에 추가하기, data가 필요 없는데 아무것도 없으면 에러나서 넣음
            questionUserSerializer = QuestionUserSerializer(
                data=QuestionsSerializer(question).data
            )
            if questionUserSerializer.is_valid():
                questionUserSerializer.save(
                    question=question,
                    user=request.user,
                )
                return Response(
                    QuestionsSerializer(question).data,
                )
            else:
                return Response(
                    questionUserSerializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                questionsSerializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
