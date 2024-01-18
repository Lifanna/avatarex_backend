# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import Group
# from django.apps import apps


# @receiver(post_save, sender=apps.get_model('main', 'CustomUser'))
# def add_user_to_group(sender, instance, created, **kwargs):
#     if created:
#         group, _ = Group.objects.get_or_create(name='Пользователь')
#         instance.groups.add(group)
