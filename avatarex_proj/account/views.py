from django.shortcuts import render
from rest_framework import generics
from . import serializers, models, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login
from account.serializers import PasswordResetSerializer, PasswordResetConfirmSerializer
from django.contrib.auth.views import PasswordResetConfirmView
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from smtplib import SMTPRecipientsRefused
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.CustomUserSerializer


class PasswordResetView(views.APIView):
    serializer_class = PasswordResetSerializer

    def send_password_reset_email(self, user):
        # Создаем токен для сброса пароля
        token_generator = PasswordResetTokenGenerator()
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        # Строим URL для восстановления пароля
        reset_url = f'{settings.BASE_URL}/password-reset-confirm/{uidb64}/{token}/'  # Измените URL на ваш фронтенд URL

        # Создаем текст сообщения
        message = f"Для восстановления пароля перейдите по ссылке: {reset_url}"

        try:
            # Отправляем письмо
            send_mail(
                'Восстановление пароля',
                message,
                'loginovmih86@mail.ru',  # замените на свой адрес электронной почты
                [user.email],
                fail_silently=False,
            )

            return Response({"detail": "Письмо для восстановления пароля отправлено на ваш адрес электронной почты."}, status=status.HTTP_200_OK)

        except SMTPRecipientsRefused as e:
            # Обработка ошибки, когда адрес получателя не существует
            return Response({"detail": "Ошибка при отправке письма: адрес получателя не существует."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = get_user_model().objects.filter(email=email).first()

        if not user:
            return Response({"detail": "Пользователь с таким email не найден"}, status=status.HTTP_404_NOT_FOUND)

        # Отправляем письмо с уникальной ссылкой для восстановления пароля
        self.send_password_reset_email(user)

        return Response({"detail": "Письмо для восстановления пароля отправлено на ваш адрес электронной почты."}, status=status.HTTP_200_OK)


 
class CustomPasswordResetConfirmView(views.APIView):
    # ваш существующий код
 
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
 
        uidb64 = serializer.validated_data['uid64']
        token = serializer.validated_data['token']
        user = self.get_user(uidb64)
        print(user)
 
        if user is None or not default_token_generator.check_token(user, token):
            # Если пользователь или токен не действительны
            return Response({"detail": "Ссылка для сброса пароля не действительна."}, status=status.HTTP_400_BAD_REQUEST)
 
        # Проверяем, что пользователь может устанавливать новый пароль
        if not user.is_active:
            return Response({"detail": "Пользователь не активен"}, status=status.HTTP_400_BAD_REQUEST)
 
        # Обновляем пароль
        user.set_password(serializer.validated_data['new_password'])
        user.save()
 
        return Response({"detail": "Пароль успешно изменен"}, status=status.HTTP_200_OK)
 
    def get_user(self, uidb64):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            return get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return None