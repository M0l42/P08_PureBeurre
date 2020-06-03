from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from purebeurre.models import UserInfos
from . import create_testing_user

import os


class SignUpTestCase(TestCase):
    def setUp(self):
        self.form = {'username': "test",
                     "first_name": "nathan",
                     "last_name": "boukobza",
                     "email": "email@email.com",
                     "password": "123456"}

    def test_sign_up_valid(self):
        old_accounts = User.objects.count()
        self.form["confirm_password"] = "123456"
        self.client.post(reverse('sign_up'), self.form)
        new_accounts = User.objects.count()
        self.assertEqual(new_accounts, old_accounts + 1)

    def test_sign_up_non_valid(self):
        old_accounts = User.objects.count()
        self.form["confirm_password"] = "abcde"
        self.client.post(reverse('sign_up'), self.form)
        new_accounts = User.objects.count()
        self.assertEqual(new_accounts, old_accounts)


class LogInTestCase(TestCase):
    def setUp(self):
        create_testing_user()

    def test_log_in_success(self):
        self.client.post(reverse('login'), {"username": "testuser", "password": "12345"})
        user = auth.get_user(self.client)
        assert user.is_authenticated

    def test_log_in_failure(self):
        self.client.post(reverse('login'), {"username": "testuser", "password": "123456"})
        user = auth.get_user(self.client)
        assert not user.is_authenticated


class LogOffTestCase(TestCase):
    def setUp(self):
        create_testing_user()

    def test_log_off(self):
        self.client.login(username='testuser', password='12345')
        self.client.get(reverse('logout'))
        user = auth.get_user(self.client)
        assert not user.is_authenticated

    def test_log_off_302(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class AccountPageTestCase(TestCase):
    def setUp(self):
        UserInfos.objects.create(user=create_testing_user())

    def test_index_page_returns_302(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)

    def test_index_page_returns_200(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)


class EditAccountPageTestCase(TestCase):
    def setUp(self):
        user_info = UserInfos.objects.create(user=create_testing_user())
        path = os.path.join(os.getcwd(), "purebeurre/tests/image_test.jpg")
        user_info.image = SimpleUploadedFile(name='image_test.jpg', content=open(path, 'rb').read(),
                                             content_type='image/jpeg')
        user_info.save()
        self.image_jpg = SimpleUploadedFile(name='image_test_2.jpg', content=open(path, 'rb').read(),
                                        content_type='image/jpeg')
        self.image_png = SimpleUploadedFile(name='image_test.png', content=open(path, 'rb').read(),
                                               content_type='image/png')

    def delete_image(self):
        self.client.login(username='testuser', password='12345', email="test@test.com")
        user = auth.get_user(self.client)
        user_info = UserInfos.objects.get(user=user)
        os.remove(user_info.image.path)

    def test_index_page_returns_302(self):
        response = self.client.get(reverse('edit-account'))
        self.assertEqual(response.status_code, 302)
        self.delete_image()

    def test_index_page_(self):
        self.client.login(username='testuser', password='12345', email="test@test.com")
        self.client.post(reverse('edit-account'), {"email": "email@email.com", "image": self.image_jpg})
        user = auth.get_user(self.client)
        user_info = UserInfos.objects.get(user=user)
        image_name = os.path.basename(user_info.image.path)
        self.assertEqual(user.email, "email@email.com")
        self.assertEqual(image_name, "testuser.jpg")
        self.delete_image()

    def test_index_page_png_image(self):
        self.client.login(username='testuser', password='12345', email="test@test.com")
        self.client.post(reverse('edit-account'), {"image": self.image_png})
        user = auth.get_user(self.client)
        user_info = UserInfos.objects.get(user=user)
        image_name = os.path.basename(user_info.image.path)
        self.assertEqual(image_name, "testuser.png")
        self.delete_image()
