from django.db import models


class Section(models.Model):

    name = models.CharField(
        max_length=30,
        verbose_name="Название материала",
        help_text="Укажите название",
    )

    description = models.TextField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Добавьте описание",
    )

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=True, related_name="sections"
    )

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"

    def __str__(self):
        return self.name


class Lesson(models.Model):

    name = models.CharField(
        max_length=30,
        verbose_name="Тема обучения",
        help_text="Укажите тему обучения",
    )

    content = models.TextField(
        max_length=500,
        verbose_name="Материал для обучения",
        help_text="Добавьте материал для обучения",
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Раздел",
        help_text="Выберите раздел",
    )

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=True, related_name="lessons"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
