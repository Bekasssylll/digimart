# Generated by Django 4.2.16 on 2024-10-06 10:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mart', '0004_apprating_opinion_alter_apprating_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='apprating',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]