# Generated by Django 4.1.7 on 2023-03-16 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[(0, 'guest'), (1, 'autorized'), (2, 'admin')], default=0, max_length=9),
        ),
    ]
