from django.contrib.auth.models import AbstractUser
from rest_framework.exceptions import NotFound


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username

    def get_object(pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def create_test_list(n: int) -> list:
        user_list = []
        for i in range(n):
            user = User.objects.create(
                username="testuser" + str(i),
            )
            user.set_password("123")
            user.save()
            user_list.append(user)
        return user_list
