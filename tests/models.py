from django.db import models

from learning.models import Section
from users.models import User


class Test(models.Model):

    name = models.CharField(
        max_length=30,
        verbose_name="Название теста",
        help_text="Укажите название теста",
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="tests",
        verbose_name="Раздел",
        help_text="Выберите раздел",
    )

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return self.name


class Question(models.Model):

    name = models.CharField(
        verbose_name="Вопрос",
        help_text="Укажите вопрос",
    )

    options = models.CharField(
        verbose_name="Варианты ответа",
        help_text="Укажите варианты ответа",
    )

    correct_answer = models.CharField()

    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, null=True, related_name="questions"
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.name


class TestAttempt(models.Model):
    user = models.ForeignKey(
        User, related_name="test_attempts", on_delete=models.CASCADE
    )
    test = models.ForeignKey(Test, related_name="attempts", on_delete=models.CASCADE)
    score = models.FloatField(null=True, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.test.name}"


class Answer(models.Model):
    attempt = models.ForeignKey(
        TestAttempt, related_name="answers", on_delete=models.CASCADE
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.CharField()

    def __str__(self):
        return f"Answer to {self.question.name} by {self.attempt.user.email}"
