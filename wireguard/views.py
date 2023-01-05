from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

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


class GetConfigFile(APIView):
    """
    Метод возвращает пир (конфиг), который не принадлежит
    ни одному пользователю.
    """

    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def __check_user_peer_exist(user):
        """ Проверяет есть ли уже пиры у пользователя или нет. """

        return WireguardPeer.objects.filter(config_owner=user).exists()

    @staticmethod
    def __link_config_to_user(user, peer):
        """ Привязывает свободный конфиг к пользователю. """

        peer.config_owner_id = user.id
        peer.save()
        return peer

    def get(self, request, *args, **kwargs):
        user = request.user
        if self.__check_user_peer_exist(user):
            user_peer = user.peers.order_by('-id')
            data = []
            for peer in user_peer:
                data.append({
                    'id': peer.id,
                    'config_file': peer.config_file
                })
            content = {'error': 'У вас уже есть конфиг файл',
                       'data': data
                       }
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        peer_without_owner = (
            WireguardPeer.objects.filter(config_owner__isnull=True)
            .order_by('id').first())
        peer = self.__link_config_to_user(user, peer_without_owner)
        content = {
            'data':
                {
                    'id': peer.id,
                    'config': peer.config_file
                }
        }

        return Response(content, status=status.HTTP_201_CREATED)
