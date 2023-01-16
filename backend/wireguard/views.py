from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.api.mixins import BaseGetApiView
from backend.wireguard.models import AllowedIp, Dns, WireguardPeer
from backend.wireguard.serializers import (ReadAllowedIpSerializer,
                                           ReadConfigsSerializer,
                                           ReadDnsSerializer)


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

    @action(detail=False, methods=('GET',), url_path='get-config')
    def get_config(self, request, *args, **kwargs):
        """
        Метод возвращает пир (конфиг), который не принадлежит
        ни одному пользователю.
        """

        user = request.user
        if self.__check_user_peer_exist(user):
            user_peer = user.peers.order_by('id').first()

            content = {
                'error': 'У вас уже есть конфиг файл',
                'data': {
                    'id': user_peer.id,
                    'config': user_peer.config_file
                }
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
