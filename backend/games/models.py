from django.db import models
from django.utils import timezone
from django.db.models import Avg
from jabacritic.settings import AUTH_USER_MODEL

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    
class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description =  models.TextField(blank=True)
    
    
class Platform(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank = True)
    
class Game(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    image = models.ImageField( #для картинки - берет из папки games_images, а загружать картинки надо в админке
        upload_to='games_images',
        blank = True,
        null = True,
        verbose_name='Обложка'
    )
    
    developer = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name = 'developed_games'
    )
    
    publisher = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name = 'published_games'
    )
    
    release_date = models.DateField(null=True, blank=True, default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) 
    
    genres = models.ManyToManyField(Genre, related_name='games')
    platforms = models.ManyToManyField(Platform, related_name='games')
    
    favorites = models.ManyToManyField(
    AUTH_USER_MODEL, # Ссылка на User
    related_name='favorite_games', # Чтобы у юзера искать user.favorite_games
    blank=True
)
    