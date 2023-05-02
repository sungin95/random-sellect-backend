from django.urls import path
from . import views

urlpatterns = [
    path("me", views.Me.as_view()),
    path("user-create", views.UserCreate.as_view()),
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
    path("change-password", views.ChangePassword.as_view()),
]
