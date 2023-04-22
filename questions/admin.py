from django.contrib import admin
from .models import Questions


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = (
        "authon",
        "count",
    )
