from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path("signin", TokenObtainPairView.as_view(), name="create-token"),
    path("signup", views.UserCreateAPIView.as_view(), name="create-user"),
    path("refresh", TokenRefreshView.as_view(), name="refresh-token"),
    path("verify", TokenVerifyView.as_view(), name="verify-token"),
    path("user-service-list", views.UserServiceListAPIView.as_view(), name="user-service-list"),
    path("password-reset", views.PasswordResetView.as_view(), name="password-reset"),
    path('password-reset/confirm', views.CustomPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('unbind-service/<int:pk>', views.CustomUserServiceDestroyView.as_view(), name='unbind-service'),
    path('bind', views.BindView.as_view(), name='bind'),
    path("user_profile", views.UserProfileAPIView.as_view(), name="user-profile"),
]
