def get_base_allowed_ip() -> object | None:
    """ Функция возвращает адрес, при котором wireguard работает всегда. """

    from wireguard.models import AllowedIp
    return AllowedIp.objects.get(ip_address__exact='0.0.0.0')


def get_all_dns() -> object | None:
    """ Функция возвращает список всех DNS адресов. """

    from wireguard.models import Dns
    return Dns.objects.all()


def get_first_wg_interface() -> object | None:
    """ Функция возвращает первый из списка WG интерфейс. """

    from wireguard.models import WireguardInterface
    return WireguardInterface.objects.first()


def get_empty_peer_ip_address() -> str:
    """ Функция проверяет, является ли новый IP дубликатом старого или нет. """

    from services.utils.ip_generator import generate_random_ip
    from wireguard.models import WireguardPeer

    last_peer_address = str(WireguardPeer.objects.last().ip_address)
    new_ip_address = str(generate_random_ip())
    if last_peer_address == new_ip_address:
        new_ip_address = str(generate_random_ip())
    return new_ip_address
