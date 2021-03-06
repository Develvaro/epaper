# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-30 15:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('epaper', '0002_auto_20161226_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mis_noticias', to='epaper.Perfil_Usuario'),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='cuerpo',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='noticias/'),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de publicaci\xf3n'),
        ),
        migrations.AlterField(
            model_name='perfil_usuario',
            name='profile_photo',
            field=models.ImageField(upload_to='perfiles/'),
        ),
    ]
