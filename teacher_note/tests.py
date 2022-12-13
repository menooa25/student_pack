from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from accounts.models import Account
from lessons.models import Building, Lesson
from teacher_note.models import Note


class TestNoteModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.teacher = get_user_model().objects.create_user(username='menooa', password='secure_one',
                                                           role=Account.TEACHER)
        cls.building = Building.objects.create(name='خارزمی')
        cls.lesson = Lesson.objects.create(name='django', building=cls.building, teacher=cls.teacher,
                                           lesson_time='10:30:00', lesson_day=2)
        cls.note = Note.objects.create(teacher=cls.teacher, lesson=cls.lesson, description='very long description')

    def test_note_created(self):
        self.assertEqual(self.note.lesson.id, self.lesson.id)
        self.assertEqual(self.note.description, 'very long description')
        self.assertEqual(self.note.teacher.id, self.teacher.id)


class TestGetNoteList(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.teacher = get_user_model().objects.create_user(username='menooa', password='secure_one',
                                                           role=Account.TEACHER)
        cls.building = Building.objects.create(name='خارزمی')
        cls.lesson = Lesson.objects.create(name='django', building=cls.building, teacher=cls.teacher,
                                           lesson_time='10:30:00', lesson_day=2)
        [Note.objects.create(teacher=cls.teacher,
                             lesson=cls.lesson,
                             description='very long description') for _ in range(5)]
        Note.objects.create(teacher=cls.teacher,
                            lesson=cls.lesson,
                            description='this is short description')

    def test_get_note_list(self):
        response = self.client.get(reverse('notes-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 6)
        self.assertEqual(response.json()[5].get('description'), 'this is short description')


class TestCreateNote(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.teacher_1 = User.objects.create_user(username='menooa', password='secure_one',
                                                 role=Account.TEACHER)
        cls.teacher_2 = User.objects.create_user(username='lucifer', password='secure_one',
                                                 role=Account.TEACHER)
        cls.building = Building.objects.create(name='خارزمی')
        cls.lesson_1 = Lesson.objects.create(name='django', building=cls.building, teacher=cls.teacher_1,
                                             lesson_time='10:30:00', lesson_day=2)
        cls.lesson_2 = Lesson.objects.create(name='mango', building=cls.building, teacher=cls.teacher_2,
                                             lesson_time='10:30:00', lesson_day=2)

    def login(self, user):
        response = self.client.post('/api/auth/jwt/create', {
            'username': user.username,
            'password': 'secure_one'
        })
        return response.json().get('access')

    def test_unauthorized_user(self):
        response = self.client.post(reverse('notes-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_with_not_owned_lesson(self):
        access_token = self.login(self.teacher_1)
        body = {
            'description': 'this is very long description',
            'lesson_id': self.lesson_2.id
        }
        response = self.client.post(reverse('notes-list'), body, HTTP_AUTHORIZATION=f'JWT {access_token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_note(self):
        access_token = self.login(self.teacher_1)
        body = {
            'description': 'this is very long description',
            'lesson_id': self.lesson_1.id
        }
        response = self.client.post(reverse('notes-list'), body, HTTP_AUTHORIZATION=f'JWT {access_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.all().count(), 1)
        created_note = Note.objects.all().first()
        self.assertEqual(created_note.description, 'this is very long description')
        self.assertEqual(created_note.teacher.id, self.teacher_1.id)


class TestUpdateNote(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.teacher_1 = User.objects.create_user(username='menooa', password='secure_one',
                                                 role=Account.TEACHER)
        cls.teacher_2 = User.objects.create_user(username='lucifer', password='secure_one',
                                                 role=Account.TEACHER)
        cls.building = Building.objects.create(name='خارزمی')
        cls.lesson_1 = Lesson.objects.create(name='django', building=cls.building, teacher=cls.teacher_1,
                                             lesson_time='10:30:00', lesson_day=2)
        cls.lesson_2 = Lesson.objects.create(name='mango', building=cls.building, teacher=cls.teacher_2,
                                             lesson_time='10:30:00', lesson_day=2)
        Note.objects.create(teacher=cls.teacher_1,
                            lesson=cls.lesson_1,
                            description='this is short description')
        Note.objects.create(teacher=cls.teacher_2,
                            lesson=cls.lesson_2,
                            description='this is short description')

    def login(self, user):
        response = self.client.post('/api/auth/jwt/create', {
            'username': user.username,
            'password': 'secure_one'
        })
        return response.json().get('access')

    def test_forbidden_update(self):
        access_token = self.login(self.teacher_1)
        response = self.client.patch(reverse('notes-detail', kwargs={'pk': 2}),
                                     HTTP_AUTHORIZATION=f'JWT {access_token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        access_token = self.login(self.teacher_1)
        body = {'description': 'uniq desc'}
        response = self.client.patch(reverse('notes-detail', kwargs={'pk': 1}), data=body,
                                     content_type='application/json',
                                     HTTP_AUTHORIZATION=f'JWT {access_token}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(Note.objects.get(id=1).description,'uniq desc')
