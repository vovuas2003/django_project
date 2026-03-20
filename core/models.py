from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Модель пользователя - расширение стандартной модели
    (пока что только добавление даты регистрации)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} (зарегистрирован {self.joined_at})"
