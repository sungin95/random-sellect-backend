# Generated by Django 4.2 on 2023-04-22 01:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sellectedQuestions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="sellectedquestion",
            name="description",
            field=models.TextField(default="1"),
            preserve_default=False,
        ),
    ]
