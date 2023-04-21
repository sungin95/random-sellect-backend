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
from .serializers import QuestionsSerializer, QuestionUserSerializer


class QuestionsList(APIView):
    def get(self, request):
        all_questions = Questions.objects.all()
        serializer = QuestionsSerializer(all_questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionsSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            return Response(
                QuestionsSerializer(question).data,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
