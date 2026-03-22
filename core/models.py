from django.db import models
from django.contrib.auth.models import User
#from django.utils import timezone

class UserProfile(models.Model):
    """
    Модель пользователя - расширение стандартной модели
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} (зарегистрирован {self.joined_at.strftime('%d.%m.%Y')})"

class TestResult(models.Model):
    """
    Модель результатов теста
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField() # количество правильных ответов из 10
    total_time_seconds = models.IntegerField() # время прохождения в секундах
    started_at = models.DateTimeField(auto_now_add=True)
    # сохраняем все 10 вопросов и правильные ответы: [{"a": 45, "b": 32, "correct": 77}, ...]
    questions = models.JSONField()
    answers = models.JSONField() # ответы пользователя: [77, 80, ...]

    def is_perfect(self):
        """
        Проверка на результат 100%
        """
        return self.score == 10

    def __str__(self):
        return f"{self.user.username} - {self.score}/10 ({self.total_time_seconds} с)"

    @classmethod
    def get_perfect_times_for_user(cls, user):
        """
        Список (номер теста, время в секундах) для идеальных тестов
        """
        perfect_tests = cls.objects.filter(user=user, score=10).order_by('started_at')
        return [
            (i + 1, test.total_time_seconds)
            for i, test in enumerate(perfect_tests)
        ]
