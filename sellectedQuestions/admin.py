from django.contrib import admin
from .models import SellectedQuestion


@admin.register(SellectedQuestion)
class SellectedQuestionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "importance",
    )
