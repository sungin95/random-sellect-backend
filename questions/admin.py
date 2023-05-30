from django.contrib import admin
from .models import Questions, SellectedQuestion


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = (
        "authon",
        "count",
    )


@admin.register(SellectedQuestion)
class SellectedQuestionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "importance",
    )
