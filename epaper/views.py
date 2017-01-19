from django.shortcuts import get_object_or_404, redirect, get_list_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import View, ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


from epaper.forms import UserCreateForm, Nueva_Noticia_Form, Busqueda, Comentario_form, Editar_Perfil_Form
from epaper.models import Noticia, Perfil_Usuario, Categoria, Comentario, Like_Noticia
# Create your views here.

def is_editor(user):
    return user.groups.filter(name="Editor").exists()


class Index(ListView):
    queryset = Noticia.objects.all().order_by('-pub_date')[:50]
    template_name = 'epaper/lista_noticias.html'
    context_object_name = 'noticias'
    paginate_by = 4
    def get_context_data(self,**kwargs):
        context = super(Index,self).get_context_data(**kwargs)
        context['titulo'] = "Home"
        return context

@method_decorator(login_required, name='dispatch')
class Perfil(View):
    template_name = 'epaper/perfil.html'
    def get(self, request, *args, **kwargs):
        perfil = get_object_or_404(Perfil_Usuario, user=request.user.pk)
        return render(request, self.template_name, {'perfil': perfil})

@method_decorator(login_required, name='dispatch')
class Editar_Perfil(View):
    template_name = 'epaper/editar_perfil.html'
    form_class = Editar_Perfil_Form
    def get(self, request, *args, **kwargs):
        perfil = get_object_or_404(Perfil_Usuario, user=request.user.pk)
        form = Editar_Perfil_Form(initial = {'nombre': perfil.user.first_name, 'apellidos': perfil.user.last_name, 'email': perfil.user.email})
        return render(request, self.template_name, {'form': form})
    def post(self, request, *args,**kwargs):
        form = self.form_class(self.request.POST, request.FILES)
        if form.is_valid():
            foto = form.cleaned_data['foto_perfil']
            if foto != None:
                perfil = get_object_or_404(Perfil_Usuario, user=request.user.pk)
                perfil.profile_photo = foto
                perfil.save()
            user = get_object_or_404(User, pk=request.user.pk)
            nombre = form.cleaned_data['nombre']
            apellidos = form.cleaned_data['apellidos']
            email = form.cleaned_data['email']
            user.first_name = nombre
            user.last_name = apellidos
            user.email = email
            user.save()
        return HttpResponseRedirect('/usuario/perfil/')

class Categoria_Lista(ListView):
    template_name = 'epaper/lista_noticias.html'
    context_object_name = 'noticias'
    paginate_by = 4

    def get_queryset(self):
        categoria = Categoria.objects.filter(categoria__iexact=self.kwargs['category'])
        if not categoria:
            noticias = Noticia.objects.none()
            return noticias
        noticias = Noticia.objects.filter(categoria = categoria).order_by('-pub_date')[:50]
        if not noticias:
            noticias = Noticia.objects.none()
        return noticias
        #category = Categoria.objects.filter(categoria__iexact=self.kwargs['category'])
        #category = get_object_or_404(Categoria, categoria__iexact=self.kwargs['category'])
    def get_context_data(self,**kwargs):
        context = super(Categoria_Lista,self).get_context_data(**kwargs)
        context['titulo'] = self.kwargs['category']
        return context

class Noticia_Detalle(DetailView):
    template_name = 'epaper/noticia.html'
    model = Noticia
    context_object_name = 'noticia'

    def get_context_data(self,**kwargs):
        context = super(Noticia_Detalle,self).get_context_data(**kwargs)
        noticia = get_object_or_404(Noticia, pk = self.kwargs['pk'])
        noticia.visitas += 1
        noticia.save()
        return context

@user_passes_test(is_editor)
def Noticia_Nueva(request):
    if request.method == 'POST':
        form = Nueva_Noticia_Form(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save(commit = False)
            candidate.autor = request.user
            candidate.save()
            return redirect('/')
    else:
        form = Nueva_Noticia_Form()
    return render(request,'epaper/noticia_nueva.html', {'form':form, 'action': "/noticia/nueva/"})

@user_passes_test(is_editor)
def Editar_Noticia(request, pk_noticia):
    redirect_to = "/noticia/" + pk_noticia
    action = "/noticia/" + pk_noticia + "/editar/"
    noticia = get_object_or_404(Noticia, pk = pk_noticia)
    if request.method == 'POST':
        form = Nueva_Noticia_Form(request.POST, request.FILES, instance = noticia)
        if form.is_valid():
            update = form.save(commit = False)
            update.save()
            return redirect(redirect_to)
    else:
        if noticia.autor == request.user:
            form = Nueva_Noticia_Form(instance = noticia)
            return render(request,'epaper/noticia_nueva.html', {'form':form, 'action':action})
        else:
            raise PermissionDenied

@user_passes_test(is_editor)
def Borrar_Noticia(request, pk_noticia):
    redirect_to = "/"
    action = "/noticia/" + pk_noticia + "/borrar/"
    noticia = get_object_or_404(Noticia, pk = pk_noticia)
    if request.method == 'POST':
        if noticia.autor == request.user:
            noticia.delete()
            return HttpResponseRedirect('/')
        else:
            raise PermissionDenied

@method_decorator(login_required, name='dispatch')
class Like_View(View):
    def get(self, request, *args, **kwargs):
        noticia = Noticia.objects.get(pk = self.kwargs['pk'])
        like = Like_Noticia.objects.filter(usuario = request.user, noticia = noticia)
        if not like:
            likenoticia = Like_Noticia(usuario = request.user, noticia=noticia)
            likenoticia.save()
            noticia.likes += 1
            noticia.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class Nuevo_Usuario(View):
    form_class = UserCreateForm
    template_name = 'epaper/registro.html'

    def dispatch(self, *args, **kwargs):
        return super(Nuevo_Usuario, self).dispatch(*args, **kwargs)

    def get(self,request,*args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save(commit = False)
            candidate.save()
            user = get_object_or_404(User, pk=candidate.pk)
            perfil = Perfil_Usuario(user = user, profile_photo = '/edia/perfiles/perfil_anonimo.png')
            perfil.save()
            return redirect('/')
        return render(request, self.template_name, {'form':form})

@login_required(redirect_field_name='/usuario/login/')
def Cambiar_Pass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/usuario/perfil/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'epaper/change_password.html', {'form': form})

class Login(View):
    template_name = 'epaper/login.html'
    redirect = '/usuario/perfil/'
    def get(self,request,*args,**kwargs):
        return render(request, self.template_name, {'redirect':self.redirect})
    def post(self,request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            #if next == "":
            next = request.POST.get('next', request.GET.get('next', ''))
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect('/usuario/perfil/')
            #else:
            #    return HttpResponseRedirect(next)
        else:
            return render(request, self.template_name)

class Salir(View):

    def get(self,request,*args,**kwargs):
        logout(request)
        return HttpResponseRedirect('/')

class Escritores_Lista(ListView):
    template_name = 'epaper/lista_escritores.html'
    context_object_name = 'escritores'
    paginate_by = 4
    queryset = Perfil_Usuario.objects.filter(user__groups__name='Editor')

class Escritor(ListView):
    queryset = Noticia.objects.all().order_by('-pub_date')[:50]
    template_name = 'epaper/lista_noticias.html'
    context_object_name = 'noticias'
    paginate_by = 4

    def get_queryset(self):
        escritor = get_object_or_404(User, username=self.kwargs['autor'])
        noticias = Noticia.objects.filter(autor = escritor).order_by('-pub_date')
        return noticias
    def get_context_data(self,**kwargs):
        context = super(Escritor,self).get_context_data(**kwargs)
        context['titulo'] = self.kwargs['autor']
        return context

class Search_by_title(ListView):
    template_name = 'epaper/lista_noticias.html'
    paginate_by = 4
    context_object_name = 'noticias'
    form_class = Busqueda

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            noticias = Noticia.objects.filter(titulo__icontains=form.cleaned_data['titulo'])
            if not noticias:
                noticias = Noticia.objects.none()
            return noticias
        noticias = Noticia.objects.none()

@method_decorator(login_required, name='dispatch')
class Nuevo_Comentario(View):
    form_class = Comentario_form
    template_name = 'epaper/noticia.html'

    def post(self,request,*args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            texto = form.cleaned_data['texto']
            noticia = get_object_or_404(Noticia, pk = kwargs['pk'])
            usuario = get_object_or_404(User, pk = request.user.pk)
            comentario = Comentario(texto = texto, noticia = noticia, usuario = usuario)
            comentario.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            raise Http404("No MyModel matches the given query.")
