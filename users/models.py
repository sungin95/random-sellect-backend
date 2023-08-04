from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username

    def create_test_list(n: int):
        user_list = []
        for i in range(n):
            user = User.objects.create(
                username="testuser" + str(i),
            )
            user.set_password("123")
            user.save()
            user_list.append(user)
        return user_list
