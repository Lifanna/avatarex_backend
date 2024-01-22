from rest_framework import serializers
from . import models


class CustomUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        user = models.CustomUser(**validated_data)
        user.set_password(password)
        user.save()

        return user

    class Meta:
        model = models.CustomUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid64 = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        # Проверяем, что новый пароль и подтверждение совпадают
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Новый пароль и подтверждение не совпадают")

        return data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
