from rest_framework import serializers

from learning.models import Lesson, Section


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для списка уроков"""

    class Meta:
        model = Lesson
        fields = ["id", "name", "content", "section"]


class LessonDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра урока"""

    class Meta:
        model = Lesson
        fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):
    """Сериализатор для списка разделов"""

    lessons = LessonSerializer(
        many=True, read_only=True, help_text="Список уроков курса"
    )
    lesson_count = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Section
        fields = ["id", "name", "description", "lesson_count", "lessons"]
        extra_kwargs = {"preview": {"read_only": True}}
