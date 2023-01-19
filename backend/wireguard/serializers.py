from rest_framework import serializers

from wireguard.models import AllowedIp, Dns, WireguardInterface, WireguardPeer


class ReadWireguardInterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WireguardInterface
        fields = ('id', 'name', 'config_file',)


class ReadAllowedIpSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowedIp
        fields = ('id', 'ip_address',)


class ReadDnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dns
        fields = ('id', 'name', 'dns_address',)


class ReadConfigsSerializer(serializers.ModelSerializer):
    wireguard_interfaces = ReadWireguardInterfaceSerializer(many=True)
    allowed_ips = ReadAllowedIpSerializer(many=True)
    dns_addresses = ReadDnsSerializer(many=True)

    class Meta:
        model = WireguardPeer
        fields = (
            'ip_address', 'ip_address_node', 'wireguard_interfaces',
            'allowed_ips',
            'dns_addresses', 'persistent_keep_alive', 'config_file',)
