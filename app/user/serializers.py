"""
Serializers for the user API view
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """update and return user"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace = False,
    )

    def validate(self, attrs):
        """Validate and authenticate users"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate (
            request = self.context.get('request'),
            username = email,
            password = password,
        )
        if not user:
            msg = _('Unable to autenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class LogoutSerializer(serializers.Serializer):
    """Verify token exists"""
    token = serializers.CharField(max_length=256)

    def validate(self, attrs):
        """validate token and get user"""
        token = attrs.get('token')
        try:
            user = Token.objects.get(key=str(token)).user
        except:
            user = None
            msg = _('Unable to find user with token')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class DeviceSerializer(serializers.ModelSerializer):
    """Serializer for device object"""
    pass
