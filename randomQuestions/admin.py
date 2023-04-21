from django.contrib import admin
from .models import Questions, QuestionUser


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = (
        "authon",
        "count",
    )


@admin.register(QuestionUser)
class QuestionUserAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "importance",
    )
