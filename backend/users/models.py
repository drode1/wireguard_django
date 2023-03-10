from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('Почта', blank=True, null=True, unique=True)
    telegram_id = models.PositiveBigIntegerField('Telegram ID', unique=True,
                                                 null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-date_joined', 'username')

    def __str__(self):
        return self.username
