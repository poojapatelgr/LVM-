# Generated by Django 4.0 on 2021-12-27 09:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('leaveman', '0010_profile_token'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Employee/Consultant Profile', 'verbose_name_plural': 'Employee/filterConsultant Profile'},
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.BooleanField(default=True, verbose_name='Consultant'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='token',
            field=models.CharField(default=uuid.UUID('aeec26ae-b33a-412d-bf0b-e04d354a9355'), max_length=500),
        ),
    ]
