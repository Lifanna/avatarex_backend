from django.contrib import admin
from . import models


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'last_login', 'created_at')
    list_display_links = ('id', 'username')
    search_fields = ('id', 'username', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'last_login', 'created_at')
    readonly_fields = ('id', 'username', 'password', 'last_login', 'is_active', 'created_at')
    save_on_top = True


admin.site.register(models.CustomUser, UserAccountAdmin)