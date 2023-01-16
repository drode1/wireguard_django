from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    """ Базовая модель. """

    created_time = models.DateTimeField('Дата создания', auto_now_add=True)
    is_active = models.BooleanField('Активен', default=True, null=False,
                                    blank=False)

    class Meta:
        abstract = True


class WireguardBaseModel(BaseModel):
    """
    Модель используемая для интерфейсов и пиров (конфигов пользователей).
    """

    private_key = models.CharField('Приватный ключ',
                                   max_length=settings.KEY_MAX_LENGTH,
                                   blank=True,
                                   unique=True)
    public_key = models.CharField('Публичный ключ',
                                  max_length=settings.KEY_MAX_LENGTH,
                                  blank=True,
                                  unique=True)

    class Meta:
        abstract = True
