from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    is_critic = models.BooleanField(
        default=False,
        verbose_name='является критиком'
    )

    description = models.TextField(
        blank = True,
        verbose_name='описание профиля'
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank = True,
        null = True,
        verbose_name='Аватар'
    )
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set", 
        related_query_name="user",
    )
    
    def __str__(self):
        return f"{self.username} ({'Критик' if self.is_critic else 'Пользователь'})"
    
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'