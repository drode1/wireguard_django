def generate_interface_peer_config_structure(public_key: str,
                                             ip_address: str,
                                             ip_address_node: str) -> str:
    """
    Функция генерирует структуру файла пира для вставки в wg интерфейс.
    Используется для дополнения wg конфигов пирами.
    """

    config = (f'\n[Peer]\n'
              f'PublicKey = {public_key}\n'
              f'AllowedIPs = {ip_address}/{ip_address_node}\n')
    return config


def generate_interface_config_structure(private_key: str, address: str,
                                        listen_port: str,
                                        network_interface: str) -> str:
    """
    Функция генерирует структуру файла для wg интерфейса.
    Используется для создания wg конфигов.
    """

    config = (f'[Interface]\n'
              f'PrivateKey = {private_key}\n'
              f'Address = {address}\n'
              f'ListenPort = {listen_port}\n'
              f'PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o {network_interface} -j MASQUERADE\n'
              f'PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o {network_interface} -j MASQUERADE\n')
    return config


def generate_interface_config_with_data(obj, peers_data) -> str:
    """
    Функция генерирует файл wg интерфейса.
    Используется для сохранения файла wg конфига.
    """

    private_key = obj.private_key
    address = f'{obj.ip_address}/{obj.ip_address_node}'
    listen_port = obj.listen_port
    network_interface = obj.server.network_interface

    config = generate_interface_config_structure(private_key, address,
                                                 listen_port,
                                                 network_interface)
    # Если передаваемый queryset не пустой, то добавляем пиры в wg интерфейс
    if len(peers_data):
        peer_list = []
        for peer in peers_data:
            peer_list.append(generate_interface_peer_config_structure(**peer))
        config += ' '.join(peer_list)
    return config


def generate_peer_config_structure(private_key: str, address: str,
                                   dns_list: str,
                                   server_public_key: str, endpoint: str,
                                   allowed_ips: str,
                                   persistent_keep_alive: int) -> str:
    """
    Функция генерирует структуру файла для пира конфига.
    Используется для создания peer конфигов.
    """

    config = (f'[Interface]\n'
              f'PrivateKey = {private_key}\n'
              f'Address = {address}\n'
              f'DNS = {dns_list}\n'
              f'[Peer]\n'
              f'PublicKey = {server_public_key}\n'
              f'Endpoint = {endpoint}\n'
              f'AllowedIPs = {allowed_ips}\n'
              f'PersistentKeepalive = {persistent_keep_alive}')
    return config


def generate_peer_config_with_data(obj) -> str:
    """
    Функция генерирует файл пир конфига.
    Используется для сохранения файла пира конфига для клиента.
    """

    private_key = obj.private_key
    address = f'{obj.ip_address}/{obj.ip_address_node}'
    dns = ','.join(
        map(str, [dns.__str__() for dns in obj.dns_addresses.all()]))
    wg_interface = obj.wireguard_interfaces.last()
    server_public_key = wg_interface.public_key
    endpoint = f'{wg_interface.server}:{wg_interface.listen_port}'
    allowed_ips = ','.join(
        map(str, [ip.__str__() for ip in obj.allowed_ips.all()]))
    persistent_keep_alive = obj.persistent_keep_alive

    config = generate_peer_config_structure(private_key, address, dns,
                                            server_public_key,
                                            endpoint, allowed_ips,
                                            persistent_keep_alive)
    return config
