from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.utils import json

from accounts.models import Account
from lessons.models import Building, Lesson, Status


class TestLessonModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.teacher = get_user_model().objects.create_user(username='menooa', password='secure_one',
                                                           role=Account.TEACHER)
        cls.building = Building.objects.create(name='خارزمی')
        cls.lesson = Lesson.objects.create(name='django', building=cls.building, teacher=cls.teacher,
                                           lesson_time='10:30:00', lesson_day=2)

    def test_models_created(self):
        self.assertEqual(self.teacher.username, 'menooa')
        self.assertEqual(self.teacher.name, None)
        self.assertEqual(str(self.building), 'خارزمی')
        self.assertEqual(self.lesson.name, 'django')
        self.assertEqual(self.lesson.lesson_day, 2)


class TestLessonApi(TestCase):
    def login(self, user, return_token=False):
        response = self.client.post('/api/auth/jwt/create', {
            'username': user.username,
            'password': 'secure_password'
        })
        if return_token:
            return response.json().get('access')
        return response

    @classmethod
    def setUpTestData(cls):
        user = get_user_model()
        cls.started_status = Status.objects.create(name='شروع شده')
        cls.not_started_status = Status.objects.create(name='شروع نشده')
        cls.user_1 = user.objects.create_user(username='user_1', password='secure_password', name='user_name_1',
                                              role=Account.TEACHER)
        cls.user_2 = user.objects.create_user(username='user_2', password='secure_password', name='user_name_2',
                                              role=Account.TEACHER)
        cls.building = Building.objects.create(name='خارزمی')
        cls.lesson_1 = Lesson.objects.create(lesson_day=2, lesson_time='09:00:00', teacher=cls.user_1,
                                             building=cls.building, name='python', status=cls.started_status)
        cls.lesson_2 = Lesson.objects.create(lesson_day=3, lesson_time='10:00:00', teacher=cls.user_2,
                                             building=cls.building, name='django', status=cls.not_started_status)

    def test_getting_lessons(self):
        response = self.client.get(reverse('lesson-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.lesson_1)
        self.assertContains(response, self.lesson_2)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_getting_auth_token(self):
        response = self.login(self.user_1)
        access_token = response.json().get('access')
        self.assertIsNotNone(access_token)
        self.assertGreater(len(access_token), 150)

    def test_get_only_user_lessons(self):
        access_token = self.login(self.user_1, True)
        lesson_list = self.client.get(reverse('lesson-list'), HTTP_AUTHORIZATION=f'JWT {access_token}')
        self.assertContains(lesson_list, self.lesson_1)
        self.assertEqual(len(lesson_list.json()), 1)
        self.assertEqual(lesson_list.json()[0].get('teacher'), self.user_1.name)

    def test_unauthorized_user_cant_create(self):
        response = self.client.post(reverse('lesson-list'), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_teacher_user_cant_create(self):
        not_teacher = get_user_model().objects.create_user(username='not_teacher', password='secure_password',
                                                           name='mr not teacher', role=Account.STUDENT)
        access_token = self.login(not_teacher, True)
        response = self.client.post(reverse('lesson-list'), {}, HTTP_AUTHORIZATION=f'JWT {access_token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_lesson_with_correct_user(self):
        body = {
            'name': 'magic lesson',
            'lesson_time': "20:00",
            'lesson_day': 6,
            'building': self.building.name,
            'status': self.started_status.name
        }
        access_token = self.login(self.user_1, True)
        response = self.client.post(reverse('lesson-list'), body, HTTP_AUTHORIZATION=f'JWT {access_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('name'), 'magic lesson')
        self.assertEqual(Lesson.objects.filter(name='magic lesson').first().teacher.id, self.user_1.id)
        self.assertEqual(Lesson.objects.count(), 3)

    def test_unauthorized_user_can_see_detail(self):
        response = self.client.get(reverse('lesson-detail', kwargs={'pk': self.lesson_1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.lesson_1)

    def test_unauthorized_user_cant_update(self):
        response = self.client.patch(reverse('lesson-detail', kwargs={'pk': self.lesson_1.id}), {}, )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_cant_delete(self):
        response = self.client.delete(reverse('lesson-detail', kwargs={'pk': self.lesson_2.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_is_not_accessible_for_every_user(self):
        not_auth_response = self.client.put(reverse('lesson-detail', kwargs={'pk': self.lesson_1.id}), {}, )
        self.assertEqual(not_auth_response.status_code, status.HTTP_401_UNAUTHORIZED)
        access_token = self.login(self.user_1, True)
        auth_response = self.client.put(reverse('lesson-detail', kwargs={'pk': self.lesson_1.id}), {},
                                        HTTP_AUTHORIZATION=f'JWT {access_token}')
        self.assertEqual(auth_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_user_can_update(self):
        access_token = self.login(self.user_1, True)
        body = {
            'name': 'new name',
        }
        response = self.client.patch(reverse('lesson-detail', kwargs={'pk': self.lesson_1.id}), data=json.dumps(body),
                                     HTTP_AUTHORIZATION=f'JWT {access_token}', content_type='application/json')
        new_lesson_1 = Lesson.objects.get(id=self.lesson_1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_lesson_1.name, 'new name')
        self.assertEqual(str(new_lesson_1.lesson_time), self.lesson_1.lesson_time)
        self.assertEqual(new_lesson_1.lesson_day, self.lesson_1.lesson_day)
        self.assertEqual(new_lesson_1.building.name, self.lesson_1.building.name)
        self.assertEqual(new_lesson_1.status.name, self.lesson_1.status.name)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_filter_by_teacher(self):
        response = self.client.get(reverse('lesson-list'), {'teacher__id': self.user_1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0].get('teacher'), self.user_1.name)

    def test_search_by_teacher(self):
        response = self.client.get(reverse('lesson-list'), {'search': self.user_1.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0].get('teacher'), self.user_1.name)
