from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path("auth/signin", TokenObtainPairView.as_view(), name="create-token"),
    path("auth/signup", views.UserCreateAPIView.as_view(), name="create-user"),
    path("auth/refresh", TokenRefreshView.as_view(), name="refresh-token"),
    path("auth/verify", TokenVerifyView.as_view(), name="verify-token"),

]