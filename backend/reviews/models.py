from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from games.models import Game, Platform
from users.models import User

class Review(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name= 'reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    platform = models.ForeignKey(
        Platform,
        on_delete=models.CASCADE
    )
    description = models.TextField(blank = False)
    is_critic = models.BooleanField(default = False)
    rating = models.IntegerField(validators=[
        MinValueValidator(0), MaxValueValidator(100)
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'game')