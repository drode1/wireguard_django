from django.contrib import admin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.html import format_html
from django_object_actions import DjangoObjectActions, action

from services.utils.config_genetrator import generate_peer_config_with_data, \
    generate_interface_config_with_data

from services.utils.keygen_generator import keygen
from wireguard.models import (AllowedIp, Dns, GeneralSettings,
                              WireguardInterface, WireguardPeer)
from django.db.models import QuerySet


@admin.register(GeneralSettings)
class SettingsAdmin(admin.ModelAdmin):
    """ Управление общими настройками. """

    list_display = ('id', 'endpoint', 'domain_name', 'network_interface',)
    list_filter = ('endpoint', 'domain_name',)


@admin.register(AllowedIp)
class AllowedIpAdmin(admin.ModelAdmin):
    """ Управление список разрешенных IP для взаимодействия с WG. """

    list_display = ('id', 'ip_address', 'is_active')
    list_filter = ('is_active',)


@admin.register(Dns)
class DnsAddressesAdmin(admin.ModelAdmin):
    """ Управление список разрешенных DNS для использования клиентом. """

    list_display = ('id', 'name', 'dns_address', 'is_active')
    list_filter = ('is_active',)


@admin.register(WireguardInterface)
class WireguardInterfaceAdmin(DjangoObjectActions, admin.ModelAdmin):
    """ Управление интерфейсами WG. """

    list_display = ('id', 'name', 'ip_address_with_node', 'server',
                    'get_quantity_of_connected_pers',
                    'download_interface_file')

    list_filter = ('is_active',)

    changelist_actions = ('generate_configs',)

    @staticmethod
    @admin.display(description='IP адрес с узлом')
    def ip_address_with_node(obj) -> str:
        """ Возвращаем IP адрес с узлом. """

        return f'{obj.ip_address}/{obj.ip_address_node}'

    @staticmethod
    @admin.display(description='Кол-во привязанных пиров')
    def get_quantity_of_connected_pers(obj) -> int:
        """ Возвращаем кол-во привязанных пиров у интерфейса. """

        return obj.interface_set.count()

    @staticmethod
    @action(description='Интерфейс')
    def download_interface_file(obj):
        """ Выводит кнопку для скачивания конфига. """

        if obj.config_file:
            return format_html(
                '<a href="{url}" download>Скачать</a>', url=obj.config_file.url
            )

    @action(label='Сгенерировать файлы')
    def generate_configs(self, request, queryset: QuerySet):
        """ По кнопке генерирует файл для каждого из интерфейсов. """

        for obj in queryset:
            if obj.config_file:
                obj.config_file.delete()
            peers_data = obj.interface_set.all().values('public_key',
                                                        'ip_address',
                                                        'ip_address_node')
            config = generate_interface_config_with_data(obj, peers_data)
            obj.config_file = default_storage.save(
                f'interfaces/{obj.name}.conf', ContentFile(config))
            obj.save()

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return self.readonly_fields
        if obj.public_key and obj.private_key:
            readonly_fields = ('public_key', 'private_key')
            return readonly_fields
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        """
        Переопределяем метод сохранения объекта для автозаполнения приватного
        и публичного ключа.
        """

        if not (obj.public_key and obj.private_key):
            obj.public_key, obj.private_key = keygen()
        super().save_model(request, obj, form, change)


@admin.register(WireguardPeer)
class WireguardPeerAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = (
        'id', 'get_ip_address_with_node', 'get_dns_addresses', 'config_owner',
        'get_wireguard_interfaces', 'download_config_file', 'is_active',)

    list_filter = ('is_active', 'wireguard_interfaces')
    changelist_actions = ('generate_configs',)

    @staticmethod
    @admin.display(description='IP адрес с узлом')
    def get_ip_address_with_node(obj):
        """ Возвращаем IP адрес с узлом. """

        return f'{obj.ip_address}/{obj.ip_address_node}'

    @staticmethod
    @admin.display(description='Список DNS адресов')
    def get_dns_addresses(obj):
        """ Выводит список DNS адресов, которые привязаны к пиру."""

        return [dns.__str__() for dns in obj.dns_addresses.all()]

    @staticmethod
    @admin.display(description='Список WG интерфейсов')
    def get_wireguard_interfaces(obj):
        """ Выводит список интерфейсов, которые привязаны к пиру."""

        return [wg for wg in obj.wireguard_interfaces.all()]

    @staticmethod
    @action(description='Конфиг')
    def download_config_file(obj):
        """ Выводит кнопку для скачивания конфига. """

        if obj.config_file:
            return format_html(
                '<a href="{url}" download>Скачать</a>', url=obj.config_file.url
            )

    @action(label='Сгенерировать файлы')
    def generate_configs(self, request, queryset: QuerySet):
        """ По кнопке генерирует файл для каждого из конфигов. """

        for obj in queryset:
            if obj.config_file:
                obj.config_file.delete()
            config = generate_peer_config_with_data(obj)
            obj.config_file = default_storage.save(f'configs/{obj.id}.conf',
                                                   ContentFile(config))
            obj.save()

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return self.readonly_fields
        if obj.public_key and obj.private_key:
            readonly_fields = ('public_key', 'private_key')
            return readonly_fields
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        """
        Переопределяем метод сохранения объекта для автозаполнения приватного
        и публичного ключа.
        """

        if not (obj.public_key and obj.private_key):
            obj.public_key, obj.private_key = keygen()
        super().save_model(request, obj, form, change)
