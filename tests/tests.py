from learning.models import Section, Lesson
from tests.models import Test, Question
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class TestSetup(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="user@user.com", password="123qwe")
        self.other_user = User.objects.create(email="user2@user.com", password="123qwe")

        self.section = Section.objects.create(
            name="материал 1", description="1234", user=self.user
        )

        self.lesson = Lesson.objects.create(
            name="урок 1",
            content="какой то предмет",
            section=self.section,
            user=self.user,
        )
        self.test = Test.objects.create(name="Тест 1", section=self.section)
        self.question = Question.objects.create(
            name="Какой то вопрос?",
            options="Тут выбор ответов",
            correct_answer="Тут верный ответ",
            test=self.test,
        )

    def authenticate(self, user=None):
        if user is None:
            user = self.user
        self.client.force_authenticate(user=user)


class TestAPITests(TestSetup):
    def test_list_tests(self):
        self.authenticate()
        url = reverse("tests:tests-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_test_notauthenticate(self):
        url = reverse("tests:tests-list")
        data = {"name": "Тест ", "section": self.section.id}
        response = self.client.post(url, data, format="json")

        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_delete_test_owner(self):
        self.authenticate()
        url = reverse("tests:tests-detail", args=[self.test.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_test_detail(self):
        self.authenticate()
        url = reverse("tests:tests-detail", args=[self.test.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Тест 1")
