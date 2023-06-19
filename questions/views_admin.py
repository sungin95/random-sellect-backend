from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Questions, SellectedQuestions
from rest_framework import status
from rest_framework.exceptions import ParseError
from django.db import transaction


class ConnectQuestion(APIView):
    @transaction.atomic(using="default")
    def get(self, request):
        if request.user.is_staff == True:
            try:
                with transaction.atomic():
                    sellected_questions = SellectedQuestions.objects.all()
                    for sq in sellected_questions:
                        qs = Questions.objects.filter(description=sq.description)
                        # 1 값 넣어줌
                        if len(qs) == 1:
                            sq.question = qs[0]
                        # 2 없으면 None
                        elif len(qs) == 0:
                            sq.question = None
                        # 3 중복되면 에러 발생(롤백한다. )
                        else:
                            raise ParseError
                        sq.save()
                    return Response(status.HTTP_200_OK)
            except:
                pass
            return Response(
                {"message": "작업도중 에러 발생"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"message": "스태프가 아님"}, status=status.HTTP_403_FORBIDDEN)
