import json

from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from accounts.models import Account

User: Account = get_user_model()


class TestAccountModel(TestCase):
    def test_create_user(self):
        User.objects.create_user(username='test_user', role=Account.TEACHER, password='secure_one')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'test_user')
        self.assertEqual(User.objects.first().role, Account.TEACHER)

    def test_login_user(self):
        User.objects.create_user(username='test_user', role=Account.TEACHER, password='secure_one', name='test_name')
        invalid_user_1 = authenticate(username='test_user1', password='secure_one')
        invalid_user_2 = authenticate(username='test_user', password='secure_one1')
        valid_user = authenticate(username='test_user', password='secure_one')
        self.assertIsNone(invalid_user_1)
        self.assertIsNone(invalid_user_2)
        self.assertIsNotNone(valid_user)
        self.assertEqual(valid_user.name, 'test_name')

    def test_update_password(self):
        User.objects.create_user(username='test_user', role=Account.TEACHER, password='secure_one', name='test_name')
        account = User.objects.filter(username='test_user').first()
        account.set_password('secure_two')
        account.save()
        invalid_user = authenticate(username='test_user', password='secure_one')
        valid_user = authenticate(username='test_user', password='secure_two')
        self.assertIsNone(invalid_user)
        self.assertIsNotNone(valid_user)


class TestUserApi(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='test_user', role=Account.TEACHER, password='secure_one',
                                             name='test_name')

    def login(self, user, return_token=False):
        response = self.client.post('/api/auth/jwt/create', {
            'username': user.username,
            'password': 'secure_one'
        })
        if return_token:
            return response.json().get('access')
        return response

    def test_get_user_info(self):
        access_token = self.login(self.user, True)
        response = self.client.get(reverse('user_detail'), HTTP_AUTHORIZATION=f'JWT {access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'test_name')
        self.assertContains(response, 'test_user')

    def test_update_user_password_validation(self):
        access_token = self.login(self.user, True)
        passwords = {'password_one': 'secure_two', 'password_two': 'secure_one'}
        response = self.client.patch(reverse('user_detail'), data=passwords, content_type='application/json',
                                     HTTP_AUTHORIZATION=f'JWT {access_token}')
        self.assertContains(response, 'The passwords are not equal', status_code=status.HTTP_400_BAD_REQUEST)

    def test_update_user_password(self):
        access_token = self.login(self.user, True)
        passwords = {'password_one': 'secure_bb', 'password_two': 'secure_bb'}
        response = self.client.patch(reverse('user_detail'), data=passwords, content_type='application/json',
                                     HTTP_AUTHORIZATION=f'JWT {access_token}')
        valid_user = authenticate(username='test_user', password='secure_bb')
        self.assertIsNotNone(valid_user)
        self.assertContains(response, 'test_name')
