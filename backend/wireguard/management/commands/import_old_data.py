import os
from csv import DictReader

from django.conf import settings as st
from django.core.management import BaseCommand
from services.decorators.decorators import print_import_file_info
from services.models.services import (get_all_dns, get_base_allowed_ip,
                                      get_first_active_wg_interface)

from users.models import User
from wireguard.models import GeneralSettings, WireguardInterface, WireguardPeer


class Command(BaseCommand):
    help = "Команда для загрузки данных из старой версии генератора wireguard"

    @staticmethod
    def _get_or_create_user(username: str | int,
                            telegram_id: int | None) -> tuple[User, bool]:
        return User.objects.get_or_create(username=username,
                                          telegram_id=telegram_id)

    @staticmethod
    def _link_wg_interface(peer: WireguardPeer) -> None:
        interface = get_first_active_wg_interface()
        if interface is None:
            raise ValueError('Отсутствует wg interface')
        interface.save()
        interface.interface_set.add(peer)
        return

    @staticmethod
    def _link_all_dns(peer: WireguardPeer) -> None:
        dns = get_all_dns()
        if dns is None:
            raise ValueError('Отсутствует dns адрес')

        for value in dns:
            value.save()
            value.dns_set.add(peer)
        return

    @staticmethod
    def _link_allowed_ip(peer: WireguardPeer) -> None:
        allowed_ip = get_base_allowed_ip()
        if allowed_ip is None:
            raise ValueError('Отсутствует разрешенный адрес')

        allowed_ip.save()
        allowed_ip.allowed_ip_set.add(peer)
        return

    @staticmethod
    def _get_or_create_peer(public_key: str, private_key: str,
                            config_owner: User, ip_address: str) -> (
            WireguardPeer, bool):
        return WireguardPeer.objects.get_or_create(
            public_key=public_key, private_key=private_key,
            config_owner=config_owner, ip_address=ip_address)

    @staticmethod
    def _import_server_data() -> None:
        """ Функция загружает данные по серверу. """

        file_path = os.path.join(st.BASE_DIR, 'static/archive/server.csv')
        with open(file_path, encoding='utf-8', mode='r') as f:
            for row in DictReader(f):
                GeneralSettings.objects.get_or_create(**row)

    @staticmethod
    def _import_interface_data() -> None:
        """ Функция загружает данные по интерфейсу. """

        file_path = os.path.join(st.BASE_DIR, 'static/archive/interface.csv')
        with open(file_path, encoding='utf-8', mode='r') as f:
            for row in DictReader(f):
                WireguardInterface.objects.get_or_create(**row)

    def _import_peer_data(self) -> None:
        """ Функция загружает данные по пирам. """

        file_path = os.path.join(st.BASE_DIR, 'static/archive/peers.csv')
        with open(file_path, encoding='utf-8', mode='r') as f:
            for row in DictReader(f):
                telegram_id = (row.get('telegram_id') if row.get(
                    'telegram_id') != '' else None)
                username = row.get('username')
                private_key = row.get('private_key')
                public_key = row.get('public_key')
                ip_address = f'10.0.0.{row.get("id")}'
                user = self._get_or_create_user(username, telegram_id)
                peer = self._get_or_create_peer(public_key, private_key,
                                                user[0], ip_address)
                self._link_wg_interface(peer[0])
                self._link_all_dns(peer[0])
                self._link_allowed_ip(peer[0])

    @print_import_file_info
    def import_data(self) -> None:
        """ Импорт базовых данных в БД при развёртывании проекта. """

        self._import_server_data()
        self._import_interface_data()
        self._import_peer_data()

    def handle(self, *args, **options):
        """
        Агрегирующий метод, который вызывается с помощью команды
        import_old_data и добавляет тестовые данные в БД.
        """

        self.import_data()
