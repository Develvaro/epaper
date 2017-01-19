"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from epaper.views import Index, Perfil, Noticia_Detalle, Nuevo_Usuario, Login, Salir, Noticia_Nueva, Categoria_Lista, Escritores_Lista, Escritor, Search_by_title, Nuevo_Comentario, Editar_Perfil, Like_View, Editar_Noticia, Borrar_Noticia, Cambiar_Pass
from django.views.generic import View
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Index.as_view(), name='index'),
    url(r'^noticia/(?P<pk>\d+)/like/$', Like_View.as_view(), name = 'like'),
    url(r'^noticia/(?P<pk_noticia>\d+)/editar/$', Editar_Noticia, name = 'editar_noticia'),
    url(r'^noticia/(?P<pk_noticia>\d+)/borrar/$', Borrar_Noticia, name = 'editar_noticia'),
    url(r'^noticia/(?P<pk>\d+)/$', Noticia_Detalle.as_view(), name='noticia'),
    url(r'^noticia/nueva/$', Noticia_Nueva, name='noticia_nueva'),
    url(r'^categoria/(?P<category>\w+)/$', Categoria_Lista.as_view(), name='categoria'),
    url(r'^usuario/perfil/?next=(?P<next>\w+)$', Perfil.as_view(), name='perfil_next'),
    url(r'^usuario/perfil/$', Perfil.as_view(), name='perfil'),
    url(r'^usuario/perfil/editar/$', Editar_Perfil.as_view(), name= 'Editar_Perfil'),
    url(r'^usuario/perfil/editar/pass/$', Cambiar_Pass, name= 'editar_pass'),
    #url(r'^usuario/perfil/favoritos/$', Perfil_Favoritos.as_view(), name= 'Editar_Perfil'),
    url(r'^usuario/nuevo/$', Nuevo_Usuario.as_view(), name='Nuevo_Usuario'),
    url(r'^usuario/login/$', Login.as_view(), name='login'),
    url(r'^usuario/salir/$', Salir.as_view(), name='salir'),
    url(r'^escritor/todos/$', Escritores_Lista.as_view(), name='lista_escritores'),
    url(r'^escritor/(?P<autor>\w+)/$', Escritor.as_view(), name = 'escritor'),
    url(r'^buscar/$', Search_by_title.as_view(), name = 'busqueda'),
    url(r'^comentario/nuevo/(?P<pk>\d+)$', Nuevo_Comentario.as_view(), name = 'Nuevo_Comentario')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
