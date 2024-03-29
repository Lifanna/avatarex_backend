from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email or password is None:
            raise ValueError('Required.')

        # email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email or password is None:
            raise ValueError('Required.')

        extra_fields['is_superuser'] = True
        extra_fields['is_staff'] = True

        # email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=12, verbose_name='Имя', null=True)
    last_name = models.CharField(max_length=12, verbose_name='Фамилия', null=True)
    is_active = models.BooleanField(default=True, verbose_name='Прошел активацию')
    is_staff = models.BooleanField(default=False, verbose_name='Служебный аккаунт')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name

    def has_perm(*args, **kwargs):
        return True

    def has_module_perms(*args, **kwargs):
        return True

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']


class Service(models.Model):
    name = models.CharField(max_length=12, verbose_name='Имя', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'


class CustomUserService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name="service")
    service_credentials = models.JSONField("Данные сервиса", default=True)
    customUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=False, verbose_name="customUser")
    created_at = models.DateTimeField(auto_now_add=True,  null=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self) -> str:
        return self.customUser.email + " / " + self.service.name

    class Meta:
        verbose_name = 'Сервис пользователя'
        verbose_name_plural = 'Сервисы пользователей'
        unique_together = ('service', 'customUser',)
