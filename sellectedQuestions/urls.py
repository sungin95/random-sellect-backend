from django.urls import path
from . import views

urlpatterns = [
    path("", views.SellectedQuestions.as_view()),
    path("<int:pk>", views.SellectQuestion.as_view()),
    path("<int:pk>/detail", views.SellectedQuestionsDetail.as_view()),
]
