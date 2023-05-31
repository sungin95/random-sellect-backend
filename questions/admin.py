from django.contrib import admin
from .models import Questions, SellectedQuestions


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = (
        "authon",
        "count",
    )


@admin.register(SellectedQuestions)
class SellectedQuestionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "importance",
    )
