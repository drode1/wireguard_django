from rest_framework import viewsets

from api.mixins import BaseGetApiView
from wireguard.models import AllowedIp, Dns, WireguardPeer
from wireguard.serializers import (ReadAllowedIpSerializer,
                                   ReadConfigsSerializer, ReadDnsSerializer)


class DnsApiView(BaseGetApiView):
    """ Класс для обработки DNS адресов. """

    serializer_class = ReadDnsSerializer
    queryset = Dns.objects.all()


class AllowedIpApiView(BaseGetApiView):
    """ Класс для обработки разрешенных IP. """

    serializer_class = ReadAllowedIpSerializer
    queryset = AllowedIp.objects.all()


class PeerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WireguardPeer.objects.all()
    serializer_class = ReadConfigsSerializer

    # TODO: Сделать проверку сериализатора на создания конфига
