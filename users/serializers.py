from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User



class CreateUserSerializer(serializers.ModelSerializer):
    """ Сериализатор используемый для создания пользователей. """

    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Пользователь с такой почтой уже существует.')]
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password',
                  )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Переопределяем метод, чтобы хэшировать пароль
        validated_data['password'] = make_password(
            validated_data.get('password')
        )
        validated_data['email'] = validated_data.get('email').lower()
        user = User.objects.create(**validated_data)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор используемый для обработки пользователей. """

    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Пользователь с такой почтой уже существует.')]
    )

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',)
