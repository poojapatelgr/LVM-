# Generated by Django 4.0 on 2021-12-27 09:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('leaveman', '0011_alter_profile_options_alter_profile_role_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='records',
            name='recname',
            field=models.CharField(default='name', max_length=75),
        ),
        migrations.AlterField(
            model_name='profile',
            name='token',
            field=models.CharField(default=uuid.UUID('62153044-a570-4eeb-b14e-db7c206158a4'), max_length=500),
        ),
    ]
