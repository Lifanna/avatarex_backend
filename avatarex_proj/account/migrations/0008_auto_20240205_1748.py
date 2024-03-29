# Generated by Django 3.2.23 on 2024-02-05 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20240205_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuserservice',
            name='customUser',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='customUser'),
        ),
        migrations.AlterField(
            model_name='customuserservice',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.service', verbose_name='service'),
        ),
        migrations.AlterUniqueTogether(
            name='customuserservice',
            unique_together={('service', 'customUser')},
        ),
    ]
