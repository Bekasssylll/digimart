# Generated by Django 4.2.16 on 2024-10-06 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mart', '0005_apprating_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apprating',
            name='app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appratings', to='mart.app'),
        ),
        migrations.CreateModel(
            name='AppComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mart.app')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]