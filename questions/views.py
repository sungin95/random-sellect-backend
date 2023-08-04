from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework import status
from .models import Questions, SellectedQuestions
from .serializers import (
    QuestionsSerializer,
    QuestionsCreateSerializer,
    SellectedQuestionSerializer,
    ShowSellectedQuestionSerializer,
    ImportanceSellectedQuestionSerializer,
)
from django.db import transaction
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from config import settings
import random
from .functions import page_nation


class TotalQuestions(APIView):
    def get(self, request):
        total_questions = Questions.objects.all().count()
        list_total_questions = [total_questions]
        return Response(list_total_questions, status.HTTP_200_OK)


class QuestionsList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, page):
        (start, end) = page_nation(request, settings.PAGE_SIZE, page)
        all_questions = Questions.objects.all().order_by("-count")[start:end]
        serializer = QuestionsSerializer(all_questions, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class QuestionCreate(APIView):
    # 질문 만들기, 나의 질문에 추가하기
    permission_classes = [IsAuthenticated]

    @transaction.atomic(using="default")
    def post(self, request):
        try:
            with transaction.atomic():
                # 질문 만들기
                questionsSerializer = QuestionsCreateSerializer(data=request.data)
                if questionsSerializer.is_valid():
                    question = questionsSerializer.save(authon=request.user)
                    # 나의 질문에 추가하기
                    questionUserSerializer = SellectedQuestionSerializer(
                        data=request.data
                    )
                    if questionUserSerializer.is_valid():
                        questionUserSerializer.save(
                            user=request.user,
                            question=question,
                        )
                        return Response(
                            QuestionsSerializer(question).data,
                            status=status.HTTP_201_CREATED,
                        )
        except:
            pass
        return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)


# 아직 사용 안하고 있음
class QuestionDelete(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Questions.objects.get(pk=pk)
        except Questions.DoesNotExist:
            raise NotFound

    def delete(self, request, questions_pk):
        question = self.get_object(questions_pk)
        # 작성자 검증
        if question.authon != request.user:
            raise PermissionDenied
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#######################################################


class TotalGetSellectedQuestions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_sellected_questions = SellectedQuestions.objects.filter(
            user=request.user
        ).count()
        list_total_sellected_questions = [total_sellected_questions]
        return Response(list_total_sellected_questions, status.HTTP_200_OK)


# 내 질문 목록 보기(get)
class GetSellectedQuestions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, page):
        (start, end) = page_nation(request, settings.PAGE_SIZE, page)
        questions = SellectedQuestions.objects.filter(
            user=request.user,
        )[start:end]
        serializer = ShowSellectedQuestionSerializer(questions, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class SellectedQuestionStart(APIView):
    permission_classes = [IsAuthenticated]

    def start(self, request):
        sellected_questions = SellectedQuestions.objects.filter(user=request.user)
        if sellected_questions.exists():
            selection_probability = [
                question.importance for question in sellected_questions
            ]

            selected_question = random.choices(
                sellected_questions, weights=selection_probability
            )[0]

            return selected_question

        else:
            # 오류를 대비해 값을 넣어 두었음.
            return {
                "pk": 0,
                "description": "질문지가 없습니다.",
                "importance": 3,
            }

    def get(self, request):
        sellectedquestion = self.start(request)
        serializer = ShowSellectedQuestionSerializer(sellectedquestion)
        return Response(serializer.data, status.HTTP_200_OK)


# 생성(post),
class SellectQuestion(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Questions.objects.get(pk=pk)
        except Questions.DoesNotExist:
            raise NotFound

    def post(self, request, questions_pk):
        question = self.get_object(questions_pk)
        questions = SellectedQuestions.objects.filter(
            user=request.user,
            description=question.description,
        )
        if len(questions) == 0:
            sellectedQuestionSerializer = SellectedQuestionSerializer(
                data=QuestionsCreateSerializer(question).data
            )
            if sellectedQuestionSerializer.is_valid():
                sellectedQuestionSerializer.save(
                    user=request.user,
                    question=question,
                )
                question.count += 1
                question.save()

                return Response(
                    sellectedQuestionSerializer.data,
                    status=status.HTTP_200_OK,
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
            return SellectedQuestions.objects.get(pk=pk)
        except SellectedQuestions.DoesNotExist:
            raise NotFound

    # importance만 처리 되도록 되어있음
    def put(self, request, sq_pk):
        sellectedQuestion = self.get_object(sq_pk)
        # 작성자 검증
        if sellectedQuestion.user != request.user:
            raise PermissionDenied
        # testcode통과를 위해 data_dict를 따로 만들었습니다.
        # request.data["importance"]를 직접 변경하니까 변경할수 없다는 에러 발생
        data_dict = {}
        if request.data["importance"]:
            data_dict["importance"] = sellectedQuestion.importance + int(
                request.data["importance"]
            )

        serializer = ImportanceSellectedQuestionSerializer(
            sellectedQuestion,
            data=data_dict,
            partial=True,
        )
        if serializer.is_valid():
            updated_importance = serializer.save()
            return Response(
                ImportanceSellectedQuestionSerializer(updated_importance).data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, sq_pk):
        sellectedQuestion = self.get_object(sq_pk)
        # 작성자 검증
        if sellectedQuestion.user != request.user:
            raise PermissionDenied
        q = sellectedQuestion.question
        q.count -= 1
        q.save()
        sellectedQuestion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
