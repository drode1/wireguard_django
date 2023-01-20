from django.conf import settings
from django.contrib import admin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import QuerySet
from django.utils.html import format_html
from django_object_actions import DjangoObjectActions, action
from services.models.services import (get_base_allowed_ip,
                                      get_empty_peer_ip_address,
                                      get_first_active_wg_interface)
from services.utils.config_genetrator import (
    generate_interface_config_with_data, generate_peer_config_with_data)
from services.utils.keygen_generator import keygen

from wireguard.models import (AllowedIp, Dns, GeneralSettings,
                              WireguardInterface, WireguardPeer)


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
    list_editable = ('ip_address',)


@admin.register(Dns)
class DnsAddressesAdmin(admin.ModelAdmin):
    """ Управление список разрешенных DNS для использования клиентом. """

    list_display = ('id', 'name', 'dns_address', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('name',)


@admin.register(WireguardInterface)
class WireguardInterfaceAdmin(DjangoObjectActions, admin.ModelAdmin):
    """ Управление интерфейсами WG. """

    list_display = ('id', 'name', 'ip_address_with_node', 'server',
                    'get_quantity_of_connected_pers',
                    'download_interface_file')

    list_filter = ('is_active',)
    changelist_actions = ('generate_interface_files',)

    fieldsets = (
        ('Общее', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('is_active', 'name',)
        }),
        ('Сервер', {
            'classes': ('wide', 'extrapretty'),
            'fields': (
                ('ip_address', 'ip_address_node'), ('server', 'listen_port'),)
        }),
        ('Ключи', {
            'classes': ('collapse',),
            'fields': ('public_key', 'private_key')
        }),
    )

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
        return None

    @action(label='Сгенерировать файлы')
    def generate_interface_files(self, request, queryset: QuerySet):
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
            return 'public_key', 'private_key', 'download_interface_file'
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
    list_per_page = settings.PEERS_PER_PAGE
    list_editable = ('config_owner',)
    changelist_actions = ('generate_config_files', 'generate_new_configs')
    save_on_top = True

    fieldsets = (
        ('Общее', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('is_active', 'config_owner',)
        }),
        ('Сервер', {
            'classes': ('wide', 'extrapretty'),
            'fields': (
                ('ip_address', 'ip_address_node'),)
        }),
        ('Привязки', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('wireguard_interfaces', 'dns_addresses', 'allowed_ips',)
        }),
        ('Ключи', {
            'classes': ('collapse',),
            'fields': ('public_key', 'private_key')
        }),
    )

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
        return None

    @action(label='Сгенерировать файлы')
    def generate_config_files(self, request, queryset: QuerySet):
        """ По кнопке генерирует файл для каждого из конфигов. """

        for obj in queryset:
            if obj.config_file:
                obj.config_file.delete()
            config = generate_peer_config_with_data(obj)
            obj.config_file = default_storage.save(f'configs/{obj.id}.conf',
                                                   ContentFile(config))
            obj.save()

    @action(label='Сгенерировать новые пиры',
            description=f'Генерирует {settings.NUMBER_OF_CONFIGS} новых пиров')
    def generate_new_configs(self, request, queryset: QuerySet):
        """ Метод генерирует новые пиры в админке автоматически. """

        for _ in range(settings.NUMBER_OF_CONFIGS):
            public_key, private_key = keygen()
            ip_address = get_empty_peer_ip_address()
            new_peer = WireguardPeer.objects.create(public_key=public_key,
                                                    private_key=private_key,
                                                    ip_address=ip_address,
                                                    )
            new_peer.wireguard_interfaces.add(get_first_active_wg_interface())
            new_peer.allowed_ips.add(get_base_allowed_ip())
            for dns in Dns.objects.all():
                new_peer.dns_addresses.add(dns.id)

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return self.readonly_fields
        if obj.public_key and obj.private_key:
            return 'public_key', 'private_key', 'download_config_file'
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        """
        Переопределяем метод сохранения объекта для автозаполнения приватного
        и публичного ключа.
        """

        if not (obj.public_key and obj.private_key):
            obj.public_key, obj.private_key = keygen()
        super().save_model(request, obj, form, change)
