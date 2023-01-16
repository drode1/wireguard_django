from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from backend.users.models import User
from backend.users.serializers import (CreateUserSerializer, UserSerializer,
                                       UserTelegramSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self) -> type[
        CreateUserSerializer | UserSerializer]:
        if self.request.method == 'POST':
            return CreateUserSerializer
        return UserSerializer


class AuthTelegramUser(CreateAPIView, RetrieveAPIView):
    """ Метод для регистрации и авторизации через Telegram. """

    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self) -> type[UserTelegramSerializer] | None:
        if self.request.method == 'POST':
            return UserTelegramSerializer
        return None

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = make_password(str(request.data.get('telegram_id')))
        User.objects.get_or_create(**serializer.validated_data,
                                   password=password)
        return Response(request.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs) -> Response:
        telegram_id = request.data.get('telegram_id')
        if telegram_id:
            user = get_object_or_404(User, telegram_id=telegram_id)
            token = AccessToken.for_user(user)
            return Response({'access': str(token)})
        return Response({'error': 'В теле запроса отсутствует telegram_id'},
                        status=status.HTTP_400_BAD_REQUEST)
