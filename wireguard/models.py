from django.core.validators import (FileExtensionValidator,
                                    validate_ipv4_address)
from django.db import models

from core.models import BaseModel, WireguardBaseModel
from users.models import User


class GeneralSettings(BaseModel):
    """ Модель для хранения базовых настроек.  """

    endpoint = models.CharField('IP адрес',
                                max_length=25,
                                default='194.68.32.97',
                                validators=[validate_ipv4_address]
                                )
    domain_name = models.CharField('Доменное имя',
                                   max_length=255,
                                   blank=True,
                                   null=True,
                                   help_text=(
                                       'Заполните поле, если хотите '
                                       'использовать доменное имя, в качестве '
                                       'адреса подключения.')
                                   )
    network_interface = models.CharField('Сетевой интерфейс', max_length=16,
                                         blank=True, null=True, default='ens3')

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'
        ordering = ('id',)

    def __str__(self):
        if self.domain_name:
            return self.domain_name
        return self.endpoint

    def __repr__(self):
        return f'Общие настройки - {self.id}'


class AllowedIp(BaseModel):
    """
    Модель для хранения разрешенных IP, для которых будет использоваться
    WG peer
    """

    ip_address = models.GenericIPAddressField('Адрес', blank=False, null=False,
                                              unique=True)

    class Meta:
        verbose_name = 'Разрешенный адрес'
        verbose_name_plural = 'Разрешенные адреса'
        ordering = ('is_active', '-id')

    def __str__(self):
        return self.ip_address

    def __repr__(self):
        return f'Адрес {self.ip_address}'


class Dns(BaseModel):
    """
    Модель для хранения DNS адресов, которые будет использовать
    WG Interface
    """

    name = models.CharField('Название ресурса', max_length=128, blank=True,
                            null=True, unique=True)

    dns_address = models.GenericIPAddressField('DNS адрес', blank=False,
                                               null=False, unique=True)

    class Meta:
        verbose_name = 'DNS адрес'
        verbose_name_plural = 'DNS адреса'
        ordering = ('is_active', '-id')

    def __str__(self):
        return self.dns_address

    def __repr__(self):
        return f'Адрес {self.name if self.name else self.dns_address}'


class WireguardInterface(WireguardBaseModel):
    """ Модель для создания wireguard интерфейсов. """

    name = models.CharField('Название интерфейса', max_length=100, unique=True,
                            default='wg0')

    listen_port = models.PositiveIntegerField('Порт', default='51820')
    ip_address = models.GenericIPAddressField('Адрес', max_length=25,
                                              default='10.0.0.0', unique=True)
    ip_address_node = models.PositiveSmallIntegerField('IP узел', default=24)

    server = models.ForeignKey(GeneralSettings, on_delete=models.SET_NULL,
                               null=True, blank=True, verbose_name='Сервер',
                               related_name='interfaces')

    config_file = models.FileField('Файл интерфейса',
                                   upload_to='interfaces/',
                                   blank=True,
                                   validators=[
                                       FileExtensionValidator(['conf'])]
                                   )

    class Meta:
        verbose_name = 'Интерфейс'
        verbose_name_plural = 'Интерфейсы'
        ordering = ('-created_time', 'name',)

    def __str__(self):
        return self.name

    def __repr__(self):
        return (
            f'Интерфейс wireguard - {self.name} '
            f'{self.ip_address}/{self.ip_address_node}')


class WireguardPeer(WireguardBaseModel):
    """ Модель для создания пользовательских пиров. """

    config_owner = models.ForeignKey(User, on_delete=models.SET_NULL,
                                     blank=True, null=True,
                                     verbose_name='Пользователь',
                                     related_name='peers')

    ip_address = models.GenericIPAddressField('Адрес', max_length=25,
                                              default='10.0.0.0', unique=True)
    ip_address_node = models.PositiveSmallIntegerField('IP узел', default=32)
    wireguard_interfaces = models.ManyToManyField(WireguardInterface,
                                                  verbose_name='Интерфейсы',
                                                  related_name='interface_set')
    allowed_ips = models.ManyToManyField(AllowedIp,
                                         verbose_name='Разрешенные адреса',
                                         related_name='allowed_ip_set')
    dns_addresses = models.ManyToManyField(Dns, verbose_name='DNS адреса',
                                           related_name='dns_set')
    persistent_keep_alive = models.PositiveSmallIntegerField(
        'Время жизни подключения', default=20
    )
    config_file = models.FileField('Конфиг файл',
                                   upload_to='configs/',
                                   blank=True,
                                   validators=[
                                       FileExtensionValidator(['conf'])]
                                   )

    class Meta:
        verbose_name = 'Пир'
        verbose_name_plural = 'Пиры'
        ordering = ('-created_time', 'id')

    def __str__(self):
        return f'{self.ip_address}/{self.ip_address_node}'

    def __repr__(self):
        return f'Пир - {self.id}'
