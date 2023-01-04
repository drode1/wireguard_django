from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django_object_actions import action

from users.models import User
from wireguard.models import WireguardPeer


class UserPeerAdminInline(admin.TabularInline):
    model = WireguardPeer
    can_delete = False
    extra = 0
    max_num = 0
    fields = ('ip_address', 'ip_address_node', 'wireguard_interfaces',
              'config_file_link',)
    verbose_name = 'Пир'
    verbose_name_plural = 'Пиры'
    readonly_fields = (
        'ip_address', 'ip_address_node', 'wireguard_interfaces',
        'config_file_link',)

    @staticmethod
    @action(description='Конфиг')
    def config_file_link(obj):
        """ Выводит кнопку для скачивания конфига. """

        if obj.config_file:
            return format_html(
                '<a href="{url}" download>Скачать</a>', url=obj.config_file.url
            )
        return '-'


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email',
                    'get_quantity_of_linked_configs',)
    list_filter = ('username', 'email',)
    inlines = (UserPeerAdminInline,)

    fieldsets = (
        ('Общее', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('is_active', 'last_login', 'date_joined',)
        }),
        ('Данные', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('first_name', 'last_name', 'username', 'email',)
        }),
        ('Права', {
            'classes': ('wide', 'extrapretty'),
            'fields': (
                ('is_staff', 'is_superuser',),)
        }),
        ('Пароль', {
            'classes': ('collapse',),
            'fields': ('password',)
        }),
    )

    @staticmethod
    @action(description='Кол-во конфигов')
    def get_quantity_of_linked_configs(obj):
        return obj.peers.count()
