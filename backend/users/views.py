from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from users.serializers import (CreateUserSerializer, UserSerializer,
                               UserTelegramSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self) -> type:
        if self.request.method == 'POST':
            return CreateUserSerializer
        return UserSerializer


class AuthTelegramUser(CreateAPIView):
    """ Метод для регистрации и авторизации через Telegram. """

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserTelegramSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserTelegramSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        telegram_id: int = serializer.validated_data.get('telegram_id')
        try:
            User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            User.objects.create(**serializer.validated_data)
        else:
            response = self._get_user_token(telegram_id)
            return response

    @staticmethod
    def _get_user_token(telegram_id: User.telegram_id):
        user = get_object_or_404(User, telegram_id=telegram_id)
        token = AccessToken.for_user(user)
        return Response({'access': str(token)}, status=status.HTTP_201_CREATED)
