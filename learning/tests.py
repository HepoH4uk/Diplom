from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


from learning.models import Section, Lesson
from users.models import User


class LearningTestSetup(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="user@user.com", password="123qwe")
        self.other_user = User.objects.create(email="user2@user.com", password="123qwe")

        self.section = Section.objects.create(
            name="Тест материал 1", description="1234", user=self.user
        )

        self.lesson = Lesson.objects.create(
            name="Тест урок 1",
            content="какой то предмет",
            section=self.section,
            user=self.user,
        )

    def authenticate(self, user=None):
        if user is None:
            user = self.user
        self.client.force_authenticate(user=user)


class SectionAPITests(LearningTestSetup):
    def test_list_sections(self):
        self.authenticate()
        url = reverse("section-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_section(self):
        self.authenticate()
        url = reverse("section-list")
        data = {"name": "Тест", "description": "Что то"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        section = Section.objects.get(id=response.data["id"])
        self.assertEqual(section.user, self.user)

    def test_create_section_notauthenticate(self):
        url = reverse("section-list")
        data = {"name": "Тест ", "description": "что то"}
        response = self.client.post(url, data, format="json")

        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_delete_section_owner(self):
        self.authenticate()
        url = reverse("section-detail", args=[self.section.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LessonAPITests(LearningTestSetup):
    def test_list_lessons(self):
        self.authenticate()
        url = reverse("lesson-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_lesson(self):
        self.authenticate()
        url = reverse("lesson-list")
        data = {"name": "Тест", "content": "Тестовый", "section": self.section.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        lesson = Lesson.objects.get(id=response.data["id"])
        self.assertEqual(lesson.user, self.user)

    def test_create_lesson_notauthenticate(self):
        url = reverse("lesson-list")
        data = {"name": "Тест", "content": "Тестовый", "section": self.section.id}
        response = self.client.post(url, data, format="json")

        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_delete_lesson_owner(self):
        self.authenticate()
        url = reverse("lesson-detail", args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
