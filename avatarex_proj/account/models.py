from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username or password is None:
            raise ValueError('Required.')

        # email = self.normalize_email(email)
        user = self.model(username=username, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if not username or password is None:
            raise ValueError('Required.')

        extra_fields['is_superuser'] = True
        extra_fields['is_staff'] = True

        # email = self.normalize_email(email)
        user = self.model(username=username, **extra_fields)

        user.set_password(password)
        user.save()

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("Логин", max_length=50, unique=True)
    # email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=12, verbose_name='Имя', null=True)
    last_name = models.CharField(max_length=12, verbose_name='Фамилия', null=True)
    is_active = models.BooleanField(default=True, verbose_name='Прошел активацию')
    is_staff = models.BooleanField(default=False, verbose_name='Служебный аккаунт')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
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
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']
