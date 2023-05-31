from django.urls import path
from . import views

urlpatterns = [
    path("", views.QuestionsList.as_view()),
    path("<int:pk>/delete", views.QuestionsDetail.as_view()),
    # sellected
    path("sellected/", views.GetSellectedQuestions.as_view()),
    path("sellected/start", views.SellectedQuestionStart.as_view()),
    path("sellected/<int:pk>", views.SellectQuestion.as_view()),
    path("sellected/<int:pk>/detail", views.SellectedQuestionsDetail.as_view()),
]
