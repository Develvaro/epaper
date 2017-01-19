# coding=utf-8

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

# Create your models here.
@python_2_unicode_compatible
class Categoria(models.Model):
    categoria = models.CharField(max_length = 200)

    def __str__(self):
        return self.categoria

@python_2_unicode_compatible
class Perfil_Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    profile_photo = models.ImageField(upload_to='perfiles/')

    def __str__(self):
        return self.user.username

@python_2_unicode_compatible
class Noticia(models.Model):
    titulo = models.CharField(max_length = 200)
    cuerpo = models.TextField()
    visitas = models.IntegerField(default = 0)
    likes = models.IntegerField(default = 0)
    pub_date = models.DateTimeField('Fecha de publicación', auto_now_add=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="noticias")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mis_noticias")
    photo = models.ImageField(upload_to="noticias/", null=True, blank=True)

    def __str__(self):
        return self.titulo

@python_2_unicode_compatible
class Comentario(models.Model):
    texto = models.TextField(max_length = 300)
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name="comentarios")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mis_comentarios")
    fecha_publicacion = models.DateTimeField('Fecha de publicación', auto_now_add=True, blank=True)

    def __str__(self):
        return self.texto

@python_2_unicode_compatible
class Like_Noticia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuario_like")
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name="noticia_like")
    fecha_like = models.DateTimeField('Fecha de like', auto_now_add=True, blank=True)

    def __str__(self):
        return self.usuario.username
