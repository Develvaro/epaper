from django.contrib import admin
from epaper.models import Categoria, Noticia, Comentario, Perfil_Usuario, Like_Noticia
# Register your models here.

admin.site.register(Categoria)
admin.site.register(Noticia)
admin.site.register(Comentario)
admin.site.register(Perfil_Usuario)
admin.site.register(Like_Noticia)
