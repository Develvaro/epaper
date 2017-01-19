# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-31 12:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('epaper', '0003_auto_20161230_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='fecha_publicacion',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Fecha de publicaci\xf3n'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='noticia',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mis_noticias', to=settings.AUTH_USER_MODEL),
        ),
    ]
