from rest_framework import serializers
from .models import Test, Question, TestAttempt, Answer


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ["id", "name", "options", "correct_answer"]


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    def create(self, validated_data):
        questions = validated_data.pop("questions")
        test = Test.objects.create(**validated_data)
        for question in questions:
            Question.objects.create(test=test, **question)
        return test

    class Meta:
        model = Test
        fields = ["id", "name", "questions", "section"]


class UserAnswerSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    selected_choice = serializers.CharField()

    def validate(self, data):
        question = data["question"]
        selected_choice = data["selected_choice"]
        if selected_choice not in question.options.split(","):
            raise serializers.ValidationError(
                "Selected choice does not belong to question"
            )
        return data


def get_score(attempt):
    correct_answers = 0
    ans = Answer.objects.filter(attempt_id=attempt.id)
    for ua in ans:
        if ua.selected_choice == ua.question.correct_answer:
            correct_answers += 1

    return (correct_answers / ans.count()) * 100


class TestAttemptCreateSerializer(serializers.ModelSerializer):
    user_answers = UserAnswerSerializer(many=True, write_only=True)

    class Meta:
        model = TestAttempt
        fields = ["id", "test", "user_answers", "score", "completed_at"]

    def create(self, validated_data):
        user_answers_data = validated_data.pop("user_answers")
        test = Test.objects.get(pk=self.context["test_id"])
        user = self.context["request"].user
        attempt = TestAttempt.objects.create(user=user, test=test)

        for ua_data in user_answers_data:
            Answer.objects.create(
                attempt=attempt,
                question=ua_data["question"],
                selected_choice=ua_data["selected_choice"],
            )
        attempt.score = get_score(attempt)
        attempt.save()
        return attempt


class TestAttemptResultSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()

    class Meta:
        model = TestAttempt
        fields = ["id", "user", "test", "score", "total_questions", "completed_at"]

    def get_score(self, attempt):
        correct_answers = 0
        ans = Answer.objects.filter(attempt_id=attempt.id)
        for ua in ans:
            if ua.selected_choice == ua.question.correct_answer:
                correct_answers += 1
        return (correct_answers / ans.count()) * 100

    def get_total_questions(self, obj):
        return obj.test.questions.count()
