from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('Почта', blank=True, unique=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-date_joined', 'username')

    def __str__(self):
        return f'{self.username}'

    def __repr__(self):
        return f'Пользователь - {self.id} {self.username}'
