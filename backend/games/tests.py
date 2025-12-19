from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Game, Company, Genre, Platform

class GameModelTest(TestCase):
    def setUp(self):
        # подготовка данных перед каждым тестом
        self.dev = Company.objects.create(name="Test Dev")
        self.pub = Company.objects.create(name="Test Pub")
        self.game = Game.objects.create(
            title="Test Game",
            description="Description",
            developer=self.dev,
            publisher=self.pub
        )

    def test_game_creation(self):
        # проверяем, что игра создалась и название совпадает
        self.assertEqual(self.game.title, "Test Game")
        self.assertEqual(self.game.developer.name, "Test Dev")

class GameAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.dev = Company.objects.create(name="CD PR")
        self.pub = Company.objects.create(name="CD PR Pub")
        Game.objects.create(title="Witcher 3", developer=self.dev, publisher=self.pub)

    def test_get_games_list(self):
        # делаем GET запрос к API
        response = self.client.get('/api/v1/games/')
        
        # проверяем, что статус 200 OK сравнивая наш код с двухсотым
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # проверяем, что вернулись данные (с учетом пагинации DRF)
        # если пагинация включена, данные лежат в response.data['results']
        # если выключена - просто response.data
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)
