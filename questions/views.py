from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework import status
from .models import Questions
from sellectedQuestions.models import SellectedQuestion
from .serializers import (
    QuestionsSerializer,
    QuestionsCreateSerializer,
)
from sellectedQuestions.serializers import SellectedQuestionSerializer
from django.db import transaction
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class QuestionsList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

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
            questionUserSerializer = SellectedQuestionSerializer(data=request.data)
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


class QuestionsDetail(APIView):
    def get_object(self, pk):
        try:
            return Questions.objects.get(pk=pk)
        except Questions.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        question = self.get_object(pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
