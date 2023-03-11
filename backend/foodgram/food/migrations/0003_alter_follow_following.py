# Generated by Django 4.1.7 on 2023-02-26 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('food', '0002_alter_isfavorite_recipe_alter_isfavorite_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='following',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
