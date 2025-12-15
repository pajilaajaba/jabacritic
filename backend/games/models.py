from django.db import models
from django.utils import timezone

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
    