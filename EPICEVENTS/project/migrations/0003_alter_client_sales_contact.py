# Generated by Django 4.0.4 on 2022-05-29 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0002_alter_event_contract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='sales_contact',
            field=models.ForeignKey(limit_choices_to={'team': 'Sale'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
