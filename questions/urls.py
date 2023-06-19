from django.urls import path
from . import views

urlpatterns = [
    path("total", views.TotalQuestions.as_view()),
    path("<int:page>", views.QuestionsList.as_view()),
    path("create", views.QuestionCreate.as_view()),
    path("delete/<int:pk>", views.QuestionDelete.as_view()),
    # sellected
    path("sellected/page/<int:page>", views.GetSellectedQuestions.as_view()),
    path("sellected/total", views.TotalGetSellectedQuestions.as_view()),
    path("sellected/start", views.SellectedQuestionStart.as_view()),
    path("sellected/<int:pk>", views.SellectQuestion.as_view()),
    path("sellected/<int:pk>/detail", views.SellectedQuestionsDetail.as_view()),
]
