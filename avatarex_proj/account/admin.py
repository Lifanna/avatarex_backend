from django.contrib import admin
from . import models


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'last_login', 'created_at')
    list_display_links = ('id', 'email')
    search_fields = ('id', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'last_login', 'created_at')
    readonly_fields = ('id', 'password', 'last_login', 'is_active', 'created_at')
    save_on_top = True


admin.site.register(models.CustomUser, UserAccountAdmin)

admin.site.register(models.Service)
admin.site.register(models.CustomUserService)