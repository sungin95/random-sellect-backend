from django.urls import path
from . import views

urlpatterns = [
    path("", views.QuestionsList.as_view()),
    path("<int:pk>/delete", views.QuestionsDetail.as_view()),
    ###
    path("", views.SellectedQuestions.as_view()),
    path("start", views.SellectedQuestionStart.as_view()),
    path("<int:pk>", views.SellectQuestion.as_view()),
    path("<int:pk>/detail", views.SellectedQuestionsDetail.as_view()),
]
