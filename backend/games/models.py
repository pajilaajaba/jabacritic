from django.db import models
from django.utils import timezone
from django.db.models import Avg

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
    
    @property #вычисляемое свойство - если оставить его как поле а не проперти, то придется каждый раз менять таблицу
    def average_rating(self):
        #берет все отзывы об игре через self и считает среднее
        ratings = self.reviews.all().aggregate(Avg('rating'))['rating__avg']
        
        if ratings is None:
            return 0
        
        return round(ratings, 1)