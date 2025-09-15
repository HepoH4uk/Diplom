from rest_framework import viewsets, permissions, filters, generics
from rest_framework.viewsets import ModelViewSet

from tests.models import Test, TestAttempt, Question
from tests.serializers import (
    TestSerializer,
    TestAttemptCreateSerializer,
    TestAttemptResultSerializer,
    QuestionSerializer,
)


class TestViewSet(ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QuestionDetailAPIView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class TestDetailAPIView(generics.RetrieveAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]


class TestAttemptCreateAPIView(generics.CreateAPIView):
    serializer_class = TestAttemptCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["test_id"] = self.kwargs["test_id"]
        return context

    def perform_create(self, serializer):
        test_id = self.kwargs.get("test_id")
        serializer.save(user=self.request.user, test_id=test_id)


class TestAttemptResultAPIView(generics.RetrieveAPIView):
    queryset = TestAttempt.objects.all()
    serializer_class = TestAttemptResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
