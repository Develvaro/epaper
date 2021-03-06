# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-26 11:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('epaper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil_Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.ImageField(upload_to='epaper/perfiles/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='noticia',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='epaper/noticias/'),
        ),
    ]
