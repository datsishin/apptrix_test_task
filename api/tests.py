from api.models import CustomUser
from django.test import TestCase


class AppTestCase(TestCase):

    def setUp(self):
        CustomUser.objects.create(first_name='Ivan', last_name='Ivanov', username='ivan_ivanov', gender='M', email='ivan@mail.ru', lon=55.55, lat=37.37)
        CustomUser.objects.create(first_name='Misha', last_name='Chico', username='misha_ivanov', gender='M', email='misha@mail.ru', lon=55.54, lat=37.36)

    def test_create_user(self):
        self.assertEqual(len(CustomUser.objects.all()), 2)

    def test_get_list_of_users(self):
        response = self.client.get('/api/list/')
        self.assertEqual(response.status_code, 200)
