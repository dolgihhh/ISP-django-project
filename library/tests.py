from django.test import TestCase

from django.urls import reverse

from .models import User



class TestUser(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('test_user', email=None, password='testpass')

    def test_get_user(self):
        user = User.objects.get(username='test_user')
        self.assertTrue(user.check_password('testpass'))

    def test_main_view(self):
        response = self.client.get(f'')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_login(self):
        login = self.client.login(username='test_user', password='testpass')
        self.client.logout()

    def test_adminclick(self):
        response = self.client.get(f'/adminclick')
        self.assertEqual(response.status_code, 200)

    def test_studentclick(self):
        response = self.client.get(f'/studentclick')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get(f'/logout')
        self.assertEqual(response.status_code, 200)
    
    def test_adminlogin(self):
        response = self.client.get(f'/adminlogin')
        self.assertEqual(response.status_code, 200)

    def test_studentlogin(self):
        response = self.client.get(f'/studentlogin')
        self.assertEqual(response.status_code, 200)

    def test_studentsignup(self):
        response = self.client.get(f'/studentsignup')
        self.assertEqual(response.status_code, 200)

    
    
