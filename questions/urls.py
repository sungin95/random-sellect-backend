from django.urls import path
from . import views

urlpatterns = [
    path("", views.QuestionsList.as_view()),
]
