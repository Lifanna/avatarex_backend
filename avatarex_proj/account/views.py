from django.shortcuts import render
from rest_framework import generics
from . import serializers, models, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import views


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.CustomUserSerializer