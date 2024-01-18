# from rest_framework import permissions


# class IsPartner(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.groups.filter(name='Партнер').exists()


# class IsCustomer(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.groups.filter(name='Пользователь').exists()
