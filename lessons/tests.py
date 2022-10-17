from django.contrib.auth import get_user_model
from django.test import TestCase

from lessons.models import Building, Lesson


class TestLessonModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.teacher = get_user_model().objects.create_user(username='menooa', password='secure_one')
        cls.building = Building.objects.create(name='خارزمی')
        cls.lesson = Lesson.objects.create(name='django', building=cls.building, teacher=cls.teacher,
                                           lesson_time='10:30:00', lesson_day=2)

    def test_models_created(self):
        self.assertEqual(self.teacher.username, 'menooa')
        self.assertEqual(self.teacher.name, None)
        self.assertEqual(str(self.building), 'خارزمی')
        self.assertEqual(self.lesson.name, 'django')
        self.assertEqual(self.lesson.lesson_day, 2)
