from tabnanny import check
from django.db import models
from games.models import Game, Platform
from users.models import User

class Review(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    platform = models.ForeignKey(
        Platform,
        on_delete=models.DO_NOTHING
    )
    description = models.TextField(blank = False)
    is_critic = models.BooleanField(default = False)
    rating = models.IntegerField()
    