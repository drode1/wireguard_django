from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from users.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """ Сериализатор используемый для создания пользователей. """

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password',
                  )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data) -> object:
        # Переопределяем метод, чтобы хэшировать пароль
        validated_data['password'] = make_password(
            validated_data.get('password'))
        validated_data['email'] = validated_data.get('email').lower()
        user = User.objects.create(**validated_data)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор используемый для обработки пользователей. """

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',)

    def update(self, instance, validated_data) -> object:
        if validated_data['email']:
            validated_data['email'] = validated_data.get('email').lower()
        return super().update(instance, validated_data)


class UserTelegramSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания пользователя через Telegram.
    """
    telegram_id = serializers.IntegerField(min_value=1, required=True)
    username = serializers.CharField(validators=[UnicodeUsernameValidator],
                                     required=True)

    class Meta:
        model = User
        fields = ('telegram_id', 'first_name', 'last_name', 'username',)
