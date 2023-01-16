from rest_framework import permissions, viewsets


class BaseGetApiView(viewsets.ReadOnlyModelViewSet):
    """ Базовый класс используемый для DNS адресов, доступных IP адресов. """

    permission_classes = (permissions.AllowAny,)
    pagination_class = None
